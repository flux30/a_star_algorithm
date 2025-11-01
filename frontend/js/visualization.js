/**
 * Graph Visualization Utilities
 * Enhanced canvas-based graph rendering with animations
 */

class GraphVisualizer {
    constructor(canvasId, graphData) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.graphData = graphData;
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.animationFrame = null;
        this.highlightedPath = [];
        this.currentNode = null;
        this.exploredNodes = new Set();
        
        this.setupCanvas();
        this.setupInteractions();
    }
    
    setupCanvas() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width - 32;
        this.canvas.height = rect.height - 32;
        
        // Calculate scale and offset to center graph
        this.calculateTransform();
    }
    
    calculateTransform() {
        const nodes = Object.values(this.graphData);
        const xs = nodes.map(n => n.x);
        const ys = nodes.map(n => n.y);
        
        const minX = Math.min(...xs);
        const maxX = Math.max(...xs);
        const minY = Math.min(...ys);
        const maxY = Math.max(...ys);
        
        const graphWidth = maxX - minX;
        const graphHeight = maxY - minY;
        
        const scaleX = (this.canvas.width * 0.8) / graphWidth;
        const scaleY = (this.canvas.height * 0.8) / graphHeight;
        this.scale = Math.min(scaleX, scaleY, 80);
        
        this.offsetX = (this.canvas.width - graphWidth * this.scale) / 2 - minX * this.scale;
        this.offsetY = (this.canvas.height - graphHeight * this.scale) / 2 - minY * this.scale;
    }
    
    setupInteractions() {
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        
        this.canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            dragStartX = e.offsetX;
            dragStartY = e.offsetY;
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
                this.offsetX += (e.offsetX - dragStartX);
                this.offsetY += (e.offsetY - dragStartY);
                dragStartX = e.offsetX;
                dragStartY = e.offsetY;
                this.draw();
            }
        });
        
        this.canvas.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            this.scale *= delta;
            this.draw();
        });
    }
    
    transformX(x) {
        return x * this.scale + this.offsetX;
    }
    
    transformY(y) {
        return y * this.scale + this.offsetY;
    }
    
    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid
        this.drawGrid();
        
        // Draw edges
        this.drawEdges();
        
        // Draw nodes
        this.drawNodes();
        
        // Draw labels
        this.drawLabels();
    }
    
    drawGrid() {
        this.ctx.strokeStyle = '#1a1a1a';
        this.ctx.lineWidth = 1;
        
        const gridSize = 50 * this.scale;
        
        for (let x = 0; x < this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y < this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }
    
    drawEdges() {
        const drawn = new Set();
        
        Object.entries(this.graphData).forEach(([nodeA, dataA]) => {
            Object.entries(dataA.neighbors || {}).forEach(([nodeB, cost]) => {
                const key = [nodeA, nodeB].sort().join('-');
                if (drawn.has(key)) return;
                drawn.add(key);
                
                const dataB = this.graphData[nodeB];
                const x1 = this.transformX(dataA.x);
                const y1 = this.transformY(dataA.y);
                const x2 = this.transformX(dataB.x);
                const y2 = this.transformY(dataB.y);
                
                // Check if edge is in highlighted path
                const isHighlighted = this.isEdgeInPath(nodeA, nodeB);
                
                this.ctx.strokeStyle = isHighlighted ? '#6366f1' : '#2d2d2d';
                this.ctx.lineWidth = isHighlighted ? 4 : 2;
                
                this.ctx.beginPath();
                this.ctx.moveTo(x1, y1);
                this.ctx.lineTo(x2, y2);
                this.ctx.stroke();
                
                // Draw cost label
                const midX = (x1 + x2) / 2;
                const midY = (y1 + y2) / 2;
                
                this.ctx.fillStyle = '#808080';
                this.ctx.font = `${12 * Math.min(this.scale / 50, 1)}px Lexend`;
                this.ctx.textAlign = 'center';
                this.ctx.fillText(cost.toFixed(1), midX, midY - 5);
            });
        });
    }
    
    drawNodes() {
        Object.entries(this.graphData).forEach(([nodeId, data]) => {
            const x = this.transformX(data.x);
            const y = this.transformY(data.y);
            const radius = 20 * Math.min(this.scale / 50, 1.5);
            
            let fillColor = '#242424';
            let strokeColor = '#6366f1';
            let strokeWidth = 2;
            
            if (nodeId === this.currentNode) {
                fillColor = '#6366f1';
                this.ctx.shadowColor = 'rgba(99, 102, 241, 0.5)';
                this.ctx.shadowBlur = 15;
                strokeWidth = 3;
            } else if (this.exploredNodes.has(nodeId)) {
                fillColor = '#10b981';
            } else if (this.highlightedPath.includes(nodeId)) {
                fillColor = '#818cf8';
            }
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
            this.ctx.fillStyle = fillColor;
            this.ctx.fill();
            this.ctx.strokeStyle = strokeColor;
            this.ctx.lineWidth = strokeWidth;
            this.ctx.stroke();
            
            this.ctx.shadowColor = 'transparent';
            this.ctx.shadowBlur = 0;
        });
    }
    
    drawLabels() {
        Object.entries(this.graphData).forEach(([nodeId, data]) => {
            const x = this.transformX(data.x);
            const y = this.transformY(data.y);
            
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = `bold ${14 * Math.min(this.scale / 50, 1.2)}px Lexend`;
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(nodeId, x, y);
        });
    }
    
    isEdgeInPath(nodeA, nodeB) {
        for (let i = 0; i < this.highlightedPath.length - 1; i++) {
            if ((this.highlightedPath[i] === nodeA && this.highlightedPath[i + 1] === nodeB) ||
                (this.highlightedPath[i] === nodeB && this.highlightedPath[i + 1] === nodeA)) {
                return true;
            }
        }
        return false;
    }
    
    setCurrentNode(nodeId) {
        this.currentNode = nodeId;
        this.draw();
    }
    
    addExploredNode(nodeId) {
        this.exploredNodes.add(nodeId);
        this.draw();
    }
    
    setHighlightedPath(path) {
        this.highlightedPath = path;
        this.draw();
    }
    
    reset() {
        this.currentNode = null;
        this.exploredNodes.clear();
        this.highlightedPath = [];
        this.draw();
    }
    
    animatePath(path, duration = 2000) {
        let index = 0;
        const interval = duration / path.length;
        
        const animate = () => {
            if (index < path.length) {
                this.setCurrentNode(path[index]);
                this.addExploredNode(path[index]);
                index++;
                setTimeout(animate, interval);
            } else {
                this.setHighlightedPath(path);
            }
        };
        
        animate();
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GraphVisualizer;
}

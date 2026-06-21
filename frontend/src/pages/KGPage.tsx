import { useState, useEffect, useCallback, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import api from '../api';

const KGPage = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [windowDims, setWindowDims] = useState({ width: 800, height: 600 });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchKG = async () => {
      try {
        const res = await api.get('/kg');
        setGraphData(res.data);
      } catch (err) {
        console.error("Failed to fetch knowledge graph", err);
      }
    };
    fetchKG();
    
    // Handle resize
    const handleResize = () => {
      if (containerRef.current) {
        setWindowDims({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight
        });
      }
    };
    
    window.addEventListener('resize', handleResize);
    handleResize();
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const paintNode = useCallback((node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const label = node.id;
    const fontSize = 12/globalScale;
    ctx.font = `${fontSize}px Sans-Serif`;
    const textWidth = ctx.measureText(label).width;
    const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

    ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
    ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = node.color || '#fff';
    ctx.fillText(label, node.x, node.y);

    node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
  }, []);

  return (
    <div className="flex flex-col gap-6 mt-4 h-[calc(100vh-140px)]">
      <div>
        <h2 className="text-3xl font-bold text-white">Knowledge Graph Topology</h2>
        <p className="text-slate-400 mt-2">Node2Vec embedded causal risk networks</p>
      </div>

      <div 
        ref={containerRef} 
        className="glass-card flex-1 overflow-hidden relative border border-slate-700 rounded-2xl"
      >
        <ForceGraph2D
          width={windowDims.width}
          height={windowDims.height}
          graphData={graphData}
          nodeLabel="id"
          nodeColor={node => node.color as string || '#3b82f6'}
          nodeRelSize={8}
          linkColor={() => 'rgba(148, 163, 184, 0.4)'}
          linkWidth={(link: any) => link.val as number || 1}
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
          nodeCanvasObject={paintNode}
          backgroundColor="#0f172a"
        />
        
        {/* Legend */}
        <div className="absolute bottom-6 left-6 glass-card p-4 bg-slate-900/80 border border-slate-700">
          <h4 className="text-sm font-bold text-white mb-3">Risk Typology</h4>
          <div className="space-y-2 text-xs">
            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#3b82f6]"></div><span>Core Object</span></div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#ef4444]"></div><span>Direct Threat</span></div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#f59e0b]"></div><span>Secondary Threat</span></div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#8b5cf6]"></div><span>External Force</span></div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#000000] border border-slate-700"></div><span>Terminal State</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KGPage;

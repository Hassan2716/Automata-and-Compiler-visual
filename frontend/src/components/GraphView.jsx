import React, { useEffect, useRef } from 'react'
import * as d3 from 'd3'

function GraphView({ data }) {
  const svgRef = useRef(null)

  useEffect(() => {
    if (!data || !svgRef.current) return

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove()

    const width = 800
    const height = 600
    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)

    // Convert states to node objects for D3
    const nodes = data.states.map((state) => ({ id: state }))
    const nodeMap = new Map(nodes.map(n => [n.id, n]))

    // Extract edges from transitions
    const edges = []
    const transitions = data.transitions || {}
    
    for (const fromState in transitions) {
      for (const symbol in transitions[fromState]) {
        const toStates = Array.isArray(transitions[fromState][symbol])
          ? transitions[fromState][symbol]
          : [transitions[fromState][symbol]]
        
        toStates.forEach((toState) => {
          if (toState && nodeMap.has(fromState) && nodeMap.has(toState)) {
            edges.push({
              source: nodeMap.get(fromState),
              target: nodeMap.get(toState),
              symbol: symbol,
            })
          }
        })
      }
    }

    // Force simulation
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        'link',
        d3
          .forceLink(edges)
          .id((d) => d.id)
          .distance(120)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))

    // Create edges (lines)
    const link = svg
      .append('g')
      .selectAll('line')
      .data(edges)
      .enter()
      .append('line')
      .attr('stroke', '#999')
      .attr('stroke-width', 2)

    // Create edge labels
    const edgeLabels = svg
      .append('g')
      .selectAll('text')
      .data(edges)
      .enter()
      .append('text')
      .text((d) => d.symbol)
      .attr('font-size', '12px')
      .attr('fill', '#333')
      .attr('text-anchor', 'middle')

    // Create nodes
    const node = svg
      .append('g')
      .selectAll('g')
      .data(nodes)
      .enter()
      .append('g')
      .call(
        d3
          .drag()
          .on('start', dragStarted)
          .on('drag', dragged)
          .on('end', dragEnded)
      )

    // Add circles for nodes
    node
      .append('circle')
      .attr('r', 25)
      .attr('fill', (d) => {
        if (data.accept_states && data.accept_states.includes(d.id)) {
          return '#10b981' // Green for accept states
        }
        return '#e5e7eb' // Gray for regular states
      })
      .attr('stroke', (d) => {
        if (d.id === data.start_state) {
          return '#3b82f6' // Blue border for start state
        }
        return '#333'
      })
      .attr('stroke-width', 2)

    // Add double circle for accept states
    node
      .filter((d) => data.accept_states && data.accept_states.includes(d.id))
      .append('circle')
      .attr('r', 20)
      .attr('fill', 'none')
      .attr('stroke', '#10b981')
      .attr('stroke-width', 2)

    // Add state labels
    node
      .append('text')
      .text((d) => d.id)
      .attr('font-size', '14px')
      .attr('text-anchor', 'middle')
      .attr('dy', 5)
      .attr('fill', '#333')
      .attr('pointer-events', 'none')
      .attr('font-weight', '500')

    // Add "START" label for start state
    node
      .filter((d) => d.id === data.start_state)
      .append('text')
      .text('START')
      .attr('font-size', '10px')
      .attr('text-anchor', 'middle')
      .attr('dy', -35)
      .attr('fill', '#3b82f6')
      .attr('font-weight', 'bold')
      .attr('pointer-events', 'none')

    // Arrow marker
    svg
      .append('defs')
      .append('marker')
      .attr('id', 'arrowhead')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 30)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#999')

    link.attr('marker-end', 'url(#arrowhead)')

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y)

      edgeLabels
        .attr('x', (d) => (d.source.x + d.target.x) / 2)
        .attr('y', (d) => (d.source.y + d.target.y) / 2 - 10)

      node.attr('transform', (d) => `translate(${d.x || 0},${d.y || 0})`)
    })

    // Drag functions
    function dragStarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    }

    function dragged(event, d) {
      d.fx = event.x
      d.fy = event.y
    }

    function dragEnded(event, d) {
      if (!event.active) simulation.alphaTarget(0)
      d.fx = null
      d.fy = null
    }

    // Cleanup
    return () => {
      simulation.stop()
    }
  }, [data])

  if (!data) return null

  return (
    <div>
      <div className="mb-4">
        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <h3 className="font-semibold mb-2">Automata Information</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium">States:</span>{' '}
              {data.states?.join(', ') || 'N/A'}
            </div>
            <div>
              <span className="font-medium">Alphabet:</span>{' '}
              {data.alphabet?.join(', ') || 'N/A'}
            </div>
            <div>
              <span className="font-medium">Start State:</span>{' '}
              {data.start_state || 'N/A'}
            </div>
            <div>
              <span className="font-medium">Accept States:</span>{' '}
              {data.accept_states?.join(', ') || 'N/A'}
            </div>
          </div>
        </div>
        {data.steps && (
          <div className="bg-blue-50 rounded-lg p-4">
            <h3 className="font-semibold mb-2">Steps:</h3>
            <ul className="list-disc list-inside text-sm">
              {data.steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div className="border border-gray-300 rounded-lg overflow-hidden bg-white">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  )
}

export default GraphView


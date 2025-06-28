'use client'
import { useState } from 'react'
import { useTimeline } from '../lib/api'
import StoryCard, { Card } from './StoryCard'
import LoadingSkeleton from './LoadingSkeleton'
import MiniMap from './MiniMap'

export default function StoryboardTimeline() {
  const { data, error } = useTimeline('?limit=100')
  const [zoom, setZoom] = useState(1)

  if (error) return <div className="p-4">Failed to load</div>
  if (!data) return <LoadingSkeleton />

  return (
    <section className="pt-16 pb-24 px-6 overflow-x-auto">
      <div className="flex justify-end gap-2 mb-4">
        <button className="border px-2" onClick={() => setZoom(z => z + 0.2)}>+
        </button>
        <button className="border px-2" onClick={() => setZoom(z => Math.max(0.4, z - 0.2))}>-
        </button>
      </div>
      <div
        className="grid auto-rows-[18rem] grid-flow-col gap-6"
        style={{ transform: `scale(${zoom})`, transformOrigin: '0 0' }}
      >
        {data.map((card: Card) => (
          <StoryCard key={card.id} card={card} />
        ))}
      </div>
      <MiniMap cards={data} zoom={zoom} />
    </section>
  )
}

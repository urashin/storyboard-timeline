'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

interface Card {
  id: number
  title: string
  excerpt: string
  image_url: string
  published: string
}

const mockCards: Card[] = [
  {
    id: 1,
    title: 'Card One',
    excerpt: 'This is the first mock card used for the prototype.',
    image_url: 'https://placehold.co/600x400',
    published: '2024-01-01',
  },
  {
    id: 2,
    title: 'Card Two',
    excerpt: 'This is the second mock card used for the prototype.',
    image_url: 'https://placehold.co/600x400',
    published: '2024-01-02',
  },
  {
    id: 3,
    title: 'Card Three',
    excerpt: 'This is the third mock card used for the prototype.',
    image_url: 'https://placehold.co/600x400',
    published: '2024-01-03',
  },
]

export default function StoryboardTimelineMock() {
  const [zoom, setZoom] = useState(1)
  return (
    <div className="p-4">
      <div className="flex justify-end gap-2 mb-4">
        <button className="border px-2" onClick={() => setZoom(z => z + 0.2)}>+
        </button>
        <button className="border px-2" onClick={() => setZoom(z => Math.max(0.4, z - 0.2))}>-
        </button>
      </div>
      <div className="flex overflow-x-auto space-x-4">
        {mockCards.map(card => (
          <motion.div
            key={card.id}
            style={{ scale: zoom }}
            className="min-w-[300px] bg-white rounded shadow p-2"
            whileHover={{ scale: zoom + 0.05 }}
          >
            <img src={card.image_url} alt="" className="mb-2 rounded" />
            <h3 className="font-bold mb-1">{card.title}</h3>
            <p className="text-sm text-gray-600">{card.excerpt}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

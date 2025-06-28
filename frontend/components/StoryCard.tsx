'use client'
/* eslint-disable @next/next/no-img-element */
import { useState } from 'react'
import { useCard, useRelate } from '../lib/api'

export interface Card {
  id: number
  title: string
  excerpt: string
  image_url: string
  published?: string
  tags?: string[]
}

export default function StoryCard({ card }: { card: Card }) {
  const [open, setOpen] = useState(false)
  const { data: full } = useCard(open ? card.id : 0)
  const { data: related } = useRelate(open ? card.id : 0)
  return (
    <>
      <div
        onClick={() => setOpen(true)}
        className="min-w-[300px] bg-white rounded shadow p-2 cursor-pointer"
      >
        {card.image_url && (
          <img src={card.image_url} alt="" className="mb-2 rounded" />
        )}
        <h3 className="font-bold mb-1">{card.title}</h3>
        <p className="text-sm text-gray-600 line-clamp-3">{card.excerpt}</p>
      </div>
      {open && (
        <div
          className="fixed inset-0 bg-black/50 flex"
          onClick={() => setOpen(false)}
        >
          <div
            className="bg-white max-w-md w-full ml-auto p-4 overflow-y-auto"
            onClick={e => e.stopPropagation()}
          >
            {full ? (
              <>
                <h2 className="text-xl font-bold mb-2">{full.title}</h2>
                <p className="mb-4 whitespace-pre-wrap">{full.excerpt}</p>
                {related && related.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-2">Related</h3>
                    <ul className="space-y-2">
                      {related.map((c: Card) => (
                        <li key={c.id}>{c.title}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            ) : (
              <p>Loading...</p>
            )}
          </div>
        </div>
      )}
    </>
  )
}

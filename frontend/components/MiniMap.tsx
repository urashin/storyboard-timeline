interface Card { id: number }

interface MiniMapProps {
  cards: Card[]
  zoom: number
}

export default function MiniMap({ cards }: MiniMapProps) {
  return (
    <div className="fixed right-4 bottom-4 p-2 bg-white/80 rounded shadow text-xs">
      {cards.length} cards
    </div>
  )
}

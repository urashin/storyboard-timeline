import useSWR from 'swr'
const fetcher = (url: string) =>
  fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`).then(r => r.json())

export const useTimeline = (query = '') =>
  useSWR(`/timeline${query}`, fetcher)

export const useCard = (id: number) =>
  useSWR(`/card/${id}`, fetcher)

export const useRelate = (id: number) =>
  useSWR(id ? `/relate/${id}` : null, fetcher)

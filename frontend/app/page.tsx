'use client'

import useSWR from 'swr'
import StoryboardTimelineMock from '../components/StoryboardTimelineMock'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function Page() {
  const { data } = useSWR(process.env.NEXT_PUBLIC_API_BASE_URL + '/timeline', fetcher)
  console.log('timeline data', data)
  return <StoryboardTimelineMock />
}

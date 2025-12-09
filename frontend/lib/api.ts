export const fetcher = (url: string) => fetch(url).then((res) => res.json());

export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

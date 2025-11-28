export interface NewsItem {
    id: number;
    title: string;
    summary: string;
    url: string;
    likes: number;
    source?: string;
    published_date?: string;
    image_url?: string;
    category?: string;
}

import { useEffect, useState } from 'react';
import axios from 'axios';
import type { NewsItem } from './types';
import { NewsCard } from './components/NewsCard';
import './index.css';

function App() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      const response = await axios.get<NewsItem[]>('http://localhost:8000/news');
      setNews(response.data);
      setError(null);
    } catch (error: any) {
      console.error("Error fetching news:", error);
      setError(error.message || "Failed to fetch news");
    } finally {
      setLoading(false);
    }
  };

  const handleLike = (id: number) => {
    setNews(prevNews => prevNews.map(item =>
      item.id === id ? { ...item, likes: item.likes + 1 } : item
    ));
  };

  if (loading) return <div className="app-container">Loading...</div>;
  if (error) return <div className="app-container" style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI News Aggregator</h1>
      </header>
      <main className="news-grid">
        {news.length === 0 ? (
          <p>No news found.</p>
        ) : (
          news.map(item => (
            <NewsCard key={item.id} item={item} onLike={handleLike} />
          ))
        )}
      </main>
    </div>
  );
}

export default App;

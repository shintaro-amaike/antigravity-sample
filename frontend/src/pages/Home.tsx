import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import type { NewsItem } from '../types';
import { NewsCard } from '../components/NewsCard';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const Home: React.FC = () => {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [updating, setUpdating] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(true);
    const LIMIT = 20;

    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

    const fetchNews = useCallback(async (reset = false) => {
        try {
            const currentPage = reset ? 0 : page;
            const skip = currentPage * LIMIT;

            if (reset) {
                setLoading(true);
                setNews([]);
            }

            const response = await axios.get<NewsItem[]>('http://localhost:8000/news', {
                params: {
                    skip,
                    limit: LIMIT,
                    q: searchQuery || undefined
                }
            });

            const newItems = response.data;
            if (newItems.length < LIMIT) {
                setHasMore(false);
            } else {
                setHasMore(true);
            }

            setNews(prev => reset ? newItems : [...prev, ...newItems]);
            if (reset) setPage(1);
            else setPage(prev => prev + 1);

            setError(null);
        } catch (error: any) {
            console.error("Error fetching news:", error);
            setError(error.message || "Failed to fetch news");
        } finally {
            setLoading(false);
        }
    }, [page, searchQuery]);

    useEffect(() => {
        fetchNews(true);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        fetchNews(true);
    };

    const handleCrawl = useCallback(async () => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }
        if (updating) return;
        try {
            setUpdating(true);
            await axios.post('http://localhost:8000/crawl');
            fetchNews(true);
        } catch (error: any) {
            console.error("Error updating news:", error);
        } finally {
            setUpdating(false);
        }
    }, [updating, fetchNews, isAuthenticated, navigate]);

    const loadMore = () => {
        if (!loading && hasMore) {
            fetchNews(false);
        }
    };

    const handleLike = (id: number) => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }
        setNews(prevNews => prevNews.map(item =>
            item.id === id ? { ...item, likes: item.likes + 1 } : item
        ));
    };

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>AI News Aggregator</h1>
                <form onSubmit={handleSearch} className="search-form">
                    <input
                        type="text"
                        placeholder="Search news..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />
                    <button type="submit" className="search-button">Search</button>
                </form>
                <button onClick={handleCrawl} disabled={updating} className="crawl-button">
                    {updating ? 'Crawling...' : 'Refresh News'}
                </button>
            </header>
            <main className="news-grid">
                {news.length === 0 && !loading ? (
                    <p>No news found.</p>
                ) : (
                    news.map(item => (
                        <NewsCard key={item.id} item={item} onLike={handleLike} />
                    ))
                )}

                {loading && <div className="loading">Loading...</div>}

                {!loading && hasMore && (
                    <button onClick={loadMore} className="load-more-button">
                        Load More
                    </button>
                )}

                {error && <div className="error">{error}</div>}
            </main>
        </div>
    );
};

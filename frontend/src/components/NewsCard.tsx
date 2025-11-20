import React from 'react';
import type { NewsItem } from '../types';
import axios from 'axios';

interface NewsCardProps {
    item: NewsItem;
    onLike: (id: number) => void;
}

export const NewsCard: React.FC<NewsCardProps> = ({ item, onLike }) => {
    const handleLike = async (e: React.MouseEvent) => {
        e.stopPropagation();
        try {
            await axios.post('http://localhost:8000/like', { id: item.id });
            onLike(item.id);
        } catch (error) {
            console.error("Error liking item:", error);
        }
    };

    return (
        <div className="news-card">
            <div className="news-content">
                <h2 className="news-title">
                    <a href={item.url} target="_blank" rel="noopener noreferrer">
                        {item.title}
                    </a>
                </h2>
                <p className="news-summary">{item.summary}</p>
            </div>
            <div className="news-footer">
                <button className="like-button" onClick={handleLike}>
                    <span className="heart-icon">♥</span> {item.likes}
                </button>
            </div>
        </div>
    );
};

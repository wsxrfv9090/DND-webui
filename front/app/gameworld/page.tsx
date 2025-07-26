'use client';

import React from 'react';
import Image from 'next/image';

// 便利贴组件
const StickyNote = ({ title, content, imageSrc, imageAlt, color = 'yellow' }) => {
  return (
    <div style={{
      backgroundColor: color === 'yellow' ? '#f9f5e9' : '#e3f2fd',
      border: color === 'yellow' ? '1px solid #e0d5b8' : '1px solid #bbdefb',
      padding: '30px',
      borderRadius: '12px',
      boxShadow: '5px 5px 15px rgba(0, 0, 0, 0.2)',
      maxWidth: '350px',
      minHeight: '450px',
      position: 'relative',
      transition: 'all 0.3s ease',
      display: 'flex',
      flexDirection: 'column',
    }} className="sticky-note">
      <div style={{
        position: 'absolute',
        top: '15px',
        right: '15px',
        width: '16px',
        height: '16px',
        borderRadius: '50%',
        backgroundColor: 'rgba(0,0,0,0.1)'
      }}></div>
      
      <h3 style={{
        marginTop: 0,
        marginBottom: '20px',
        borderBottom: '2px solid rgba(0,0,0,0.1)',
        paddingBottom: '10px',
        fontFamily: '"Permanent Marker", cursive',
        fontSize: '24px',
        color: '#333',
        textAlign: 'center'
      }}>{title}</h3>
      
      <div style={{
        width: '100%',
        height: '180px',
        position: 'relative',
        marginBottom: '15px',
        borderRadius: '8px',
        overflow: 'hidden',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <Image 
          src={imageSrc} 
          alt={imageAlt} 
          fill
          style={{
            objectFit: 'cover',
          }}
        />
      </div>
      
      <div style={{
        fontFamily: '"Comic Sans MS", "Marker Felt", cursive, sans-serif',
        fontSize: '16px',
        lineHeight: '1.6',
        color: '#444',
        flexGrow: 1,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
      }}>
        <div>{content}</div>
      </div>
    </div>
  );
};

// 游戏世界页面
export default function GameWorld() {
  // 游戏世界数据
  const worldNotes = [
    {
      id: 1,
      title: '我们的Avatar',
      content: '关于我们',
      imageSrc: '/avatar.png',
      imageAlt: '游戏角色',
      color: 'yellow'
    },
    {
      id: 2,
      title: '游戏Logo',
      content: '这是我们的游戏标志，象征着冒险与未知的旅程。',
      imageSrc: '/logo.png',
      imageAlt: '游戏标志',
      color: 'blue'
    },
    {
      id: 3,
      title: '场景一',
      content: '探索这个事件背后的真相，发现隐藏的秘密。',
      imageSrc: '/photo1.jpg',
      imageAlt: '游戏场景一',
      color: 'yellow'
    },
    {
      id: 4,
      title: '场景二',
      content: '另一个令人惊叹的地点，充满了挑战和冒险。',
      imageSrc: '/photo2.jpg',
      imageAlt: '游戏场景二',
      color: 'blue'
    }
  ];

  return (
    <div style={{
      minHeight: '100vh',
      padding: '40px 20px',
      backgroundColor: '#f0f0e8',
      backgroundImage: 'linear-gradient(#e5e5e5 1px, transparent 1px), linear-gradient(90deg, #e5e5e5 1px, transparent 1px)',
      backgroundSize: '40px 40px',
      fontFamily: '"Comic Sans MS", "Marker Felt", cursive, sans-serif'
    }}>
      <h1 style={{
        textAlign: 'center',
        marginBottom: '40px',
        color: '#333',
        fontFamily: '"Permanent Marker", cursive',
        textShadow: '1px 1px 2px rgba(0,0,0,0.1)',
        fontSize: '48px'
      }}>游戏世界</h1>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '30px',
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '0 20px'
      }}>
        {worldNotes.map(note => (
          <StickyNote
            key={note.id}
            title={note.title}
            content={note.content}
            imageSrc={note.imageSrc}
            imageAlt={note.imageAlt}
            color={note.color}
          />
        ))}
      </div>
      
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
        
        .sticky-note {
          transition: all 0.3s ease;
        }
        
        .sticky-note:hover {
          transform: translateY(-5px);
          box-shadow: 8px 8px 25px rgba(0, 0, 0, 0.15) !important;
          z-index: 10;
        }
      `}</style>
    </div>
  );
}

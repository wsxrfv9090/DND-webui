'use client';

import React from 'react';
import { skills } from './skillsData';

// 便利贴组件
const StickyNote = ({ title, content, color = 'yellow' }) => {
  return (
    <div style={{
      backgroundColor: color === 'yellow' ? '#f9f5e9' : '#e3f2fd',
      border: color === 'yellow' ? '1px solid #e0d5b8' : '1px solid #bbdefb',
      padding: '40px',
      borderRadius: '12px',
      boxShadow: '5px 5px 15px rgba(0, 0, 0, 0.2)',
      maxWidth: '800px',
      minHeight: '500px',
      position: 'relative',
      transition: 'all 0.3s ease',
      margin: '0 auto',
    }} className="sticky-note">
      <div style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        width: '20px',
        height: '20px',
        borderRadius: '50%',
        backgroundColor: 'rgba(0,0,0,0.1)'
      }}></div>
      <h3 style={{
        marginTop: 0,
        marginBottom: '30px',
        borderBottom: '2px solid rgba(0,0,0,0.1)',
        paddingBottom: '15px',
        fontFamily: '"Permanent Marker", cursive',
        fontSize: '32px',
        color: '#333',
        textAlign: 'center'
      }}>{title}</h3>
      <div style={{
        fontFamily: '"Comic Sans MS", "Marker Felt", cursive, sans-serif',
        fontSize: '20px',
        lineHeight: '1.8',
        color: '#444',
        padding: '0 20px'
      }}>{content}</div>
    </div>
  );
};

// 游戏信息页面
export default function GameInformation() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
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
      }}>游戏手册</h1>
      
      <StickyNote 
        title="技能介绍"
        color="yellow"
        content={
          <div>
            <p>欢迎来到游戏指南！在这里你可以找到游戏内容的相关信息</p>
            <p>以下是所有的技能列表：</p>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
              gap: '10px',
              marginTop: '20px'
            }}>
              {skills.map((skill, index) => (
                <div key={index} style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.3)',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  textAlign: 'center',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                  transition: 'all 0.2s ease'
                }}>
                  {skill}
                </div>
              ))}
            </div>
            <p style={{ marginTop: '30px', fontStyle: 'italic' }}>
              更多内容敬请期待...
            </p>
          </div>
        }
      />
      
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
        
        .sticky-note {
          transition: all 0.3s ease;
        }
        
        .sticky-note:hover {
          transform: translateY(-5px);
          box-shadow: 8px 8px 25px rgba(0, 0, 0, 0.15) !important;
        }
      `}</style>
    </div>
  );
}
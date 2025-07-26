'use client';
// 引入 Next.js 的图片组件
import Image from "next/image";
// 引入 Next.js 的路由钩子，用于页面跳转
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

// Import fonts globally for this page
import './page_fonts.css';

export default function Home() {
  const router = useRouter();
  const [mainTitle, setMainTitle] = useState('');
  const [subTitle, setSubTitle] = useState('');
  const [showCursorMain, setShowCursorMain] = useState(true);
  const [showCursorSub, setShowCursorSub] = useState(false);
  const [showStory, setShowStory] = useState(false);
  const [displayedText, setDisplayedText] = useState('');
  const storyLines = [
    '【主线故事】',
    '在遥远的未来，人类文明已经发展到了星际时代。',
    '你，一位年轻的探险家，意外发现了一个被遗忘的星球...',
    '随着飞船降落在星球表面，你发现了一座巨大的古老遗迹。',
    '墙壁上刻满了未知的文字，似乎隐藏着重要的秘密...',
    '在遗迹的最深处，你发现了一个惊人的真相...',
    '这个发现将永远改变人类对宇宙的认知。'
  ];
  const [currentLine, setCurrentLine] = useState(0);
  const [currentText, setCurrentText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [showClickHint, setShowClickHint] = useState(false);

  const fullMainTitle = 'Welcome to AllStorys';
  
  // 处理打字效果
  useEffect(() => {
    if (!showStory) return;
    
    if (currentLine < storyLines.length) {
      setIsTyping(true);
      setShowClickHint(false);
      const line = storyLines[currentLine];
      let i = 0;
      setCurrentText(''); // 清空当前文本
      
      const typingInterval = setInterval(() => {
        if (i < line.length) {
          setCurrentText(prev => prev + line.charAt(i));
          i++;
        } else {
          clearInterval(typingInterval);
          setIsTyping(false);
          setShowClickHint(true);
        }
      }, 50);
      
      return () => clearInterval(typingInterval);
    }
  }, [showStory, currentLine]);
  
  // 处理点击事件
  const handleStoryClick = () => {
    // 如果正在打字，完成当前行
    if (isTyping) {
      const line = storyLines[currentLine];
      setCurrentText(line);
      setIsTyping(false);
      setShowClickHint(true);
      return;
    }
    
    // 如果是最后一行，淡出并跳转
    if (currentLine >= storyLines.length - 1) {
      setIsFadingOut(true);
      setTimeout(() => {
        router.push('/AIchatcoc');
      }, 1000);
      return;
    }
    
    // 继续下一行
    setCurrentLine(prev => prev + 1);
    setShowClickHint(false);
  };

  const handleStartClick = () => {
    setShowStory(true);
    setCurrentLine(0);
    setCurrentText('');
    setIsFadingOut(false);
    setShowClickHint(false);
  };
  const fullSubTitle = '... Made by us ...';

  useEffect(() => {
    let i = 0;
    const typingInterval = setInterval(() => {
      if (i < fullMainTitle.length) {
        setMainTitle(prev => prev + fullMainTitle.charAt(i));
        i++;
      } else {
        clearInterval(typingInterval);
        setShowCursorMain(false);
        setShowCursorSub(true);
        // Start subtitle typing
        let j = 0;
        const subTypingInterval = setInterval(() => {
          if (j < fullSubTitle.length) {
            setSubTitle(prev => prev + fullSubTitle.charAt(j));
            j++;
          } else {
            clearInterval(subTypingInterval);
            setShowCursorSub(false);
          }
        }, 120);
      }
    }, 150);

    return () => {
      clearInterval(typingInterval);
    };
  }, []);

  return (
    <>
      <div className="page-container">
        <header className="page-header">
          <div className="logo">
            <span className="logo-icon">N</span>
            <span>Game Agent</span>
          </div>
          <nav className="navigation">
            {['游戏世界', '职业手册', '团队', '社区'].map((item) => (
              <button key={item} className="nav-button">
                {item}
              </button>
            ))}
          </nav>
        </header>

        <main className="main-content">
          <h1 className="main-title">
            {mainTitle}
            {showCursorMain && <span className="cursor">|</span>}
          </h1>
          <div className="subtitle">
            {subTitle}
            {showCursorSub && <span className="cursor">|</span>}
          </div>
          <button 
            className="start-btn" 
            onClick={handleStartClick}
          >
            探寻真相
          </button>
          
          {showStory && (
            <div 
              className={`story-overlay ${isFadingOut ? 'fade-out' : ''}`}
              onClick={handleStoryClick}
              style={{ cursor: 'pointer' }}
            >
              <div className="story-content">
                {currentLine < storyLines.length && (
                  <p>
                    {currentText}
                    <span className={`cursor ${isTyping ? 'blinking' : ''}`}>|</span>
                  </p>
                )}
                {showClickHint && (
                  <p className="click-hint">
                    {currentLine < storyLines.length - 1 ? '继续探寻...' : '点击开始探寻...'}
                  </p>
                )}
              </div>
            </div>
          )}
        </main>
        
        <div className="vignette"></div>
        <div className="symbols-overlay"></div>

        <style jsx>{`
          .page-container {
            min-height: 100vh;
            font-family: 'Lato', sans-serif;
            color: #d2c8b8; /* Faded text color */
            background-color: #1a2a2a; /* Dark green-blue base */
            background-image: 
              linear-gradient(rgba(26, 42, 42, 0.9), rgba(15, 25, 35, 0.9)),
              url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Cg fill="%239C92AC" fill-opacity="0.05"%3E%3Crect x="0" y="0" width="100" height="100"/%3E%3C/g%3E%3C/svg%3E'); /* Subtle pattern */
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow: hidden;
            border: 12px solid #1a1412;
            box-shadow: inset 0 0 40px rgba(0,0,0,0.7);
          }
          .page-container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXWBgYGHh4d5eXlzc3OLi4ubm5uVlZWPj4+NjY19fX2JiYl/f39sbGxvb29paP9qaa5prrJdoM9doM5doM4+PpGvAAAAOXRSTlMADRAnL0BRX2d0k5Wcpa6/xM/X29/p8vX4+vv8/f7/f39/f39/f39/f39/f39/f39/f38AAABiSURBVEjH7dY3CoAgGATgJj1Vp2q3m/3/v6QZJJs3k4B6gM2wU2S2ODs6c5o2h22gKxrs1v2/pIlp2+1pW3b39b+3a3zW5jK3P+4x2sO/vL21s+6s+9h/de/y/f4A/Ie5uUAAAAASUVORK5CYII=');
            opacity: 0.15;
            mix-blend-mode: overlay;
            pointer-events: none;
          }
          .vignette {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            box-shadow: inset 0 0 15vw rgba(10, 5, 15, 0.8); /* Dark purple vignette */
            pointer-events: none;
          }
          .page-header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 48px;
            background: rgba(10, 5, 15, 0.2);
            border-bottom: 1px solid rgba(172, 94, 75, 0.3); /* Rusty red accent */
            backdrop-filter: blur(3px);
            z-index: 10;
          }
          .logo {
            font-family: 'Cormorant', serif;
            font-size: 28px;
            font-weight: 700;
            color: #e0d8c8;
            display: flex; align-items: center; gap: 12px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
          }
          .logo-icon {
            border: 2px solid rgba(172, 94, 75, 0.5);
            padding: 2px 10px;
            border-radius: 4px;
          }
          .nav-button {
            font-family: 'Lato', sans-serif;
            background: transparent;
            border: none;
            color: #b8a898;
            font-size: 18px;
            font-weight: 700;
            padding: 8px 16px;
            cursor: pointer;
            transition: color 0.3s, text-shadow 0.3s;
            position: relative;
          }
          .nav-button::after {
            content: '';
            position: absolute;
            bottom: 0; left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 2px;
            background: #ac5e4b; /* Rusty red */
            transition: width 0.3s;
          }
          .nav-button:hover {
            color: #e0d8c8;
            text-shadow: 0 0 8px rgba(172, 94, 75, 0.5);
          }
          .nav-button:hover::after {
            width: 100%;
          }
          .main-content {
            flex: 1; display: flex; flex-direction: column;
            justify-content: center; align-items: center; text-align: center;
            padding: 0 2rem; z-index: 1;
          }
          .main-title {
            font-family: 'Cormorant', serif;
            font-size: clamp(3rem, 8vw, 5.5rem);
            font-weight: 700;
            color: #e0d8c8;
            text-shadow: 0 2px 5px rgba(0,0,0,0.6);
            margin: 0;
            letter-spacing: 2px;
          }
          .subtitle {
            font-family: 'Lato', sans-serif;
            font-size: 24px;
            color: #a89888;
            margin-top: 1rem;
            margin-bottom: 3rem;
            letter-spacing: 1px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
          }
          .cursor {
            animation: blink 1s step-end infinite;
            font-weight: 400;
          }
          @keyframes blink {
            from, to { opacity: 1; }
            50% { opacity: 0; }
          }
          .start-btn {
            font-family: 'Cormorant', serif;
            font-size: 28px;
            font-weight: 700;
            color: #d2c8b8;
            background: transparent;
            border: 3px solid rgba(172, 94, 75, 0.6);
            padding: 12px 32px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 0 rgba(172, 94, 75, 0.4);
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
          }
          .start-btn:hover {
            background: rgba(172, 94, 75, 0.1);
            color: #fff;
            border-color: #ac5e4b;
            box-shadow: 0 0 20px rgba(172, 94, 75, 0.4);
            transform: translateY(-3px);
          }
          
          .story-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: #000;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.5s ease-in-out forwards;
          }
          
          .story-overlay.fade-out {
            animation: fadeOut 1s ease-in-out forwards;
          }
          
          .click-hint {
            margin-top: 2rem;
            opacity: 0.7;
            font-size: 1.2rem;
            animation: pulse 2s infinite;
          }
          
          @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
          }
          
          .story-content {
            color: #fff;
            font-size: 2rem;
            text-align: center;
            line-height: 1.8;
            max-width: 80%;
            font-family: 'Courier New', monospace;
          }
          
          .story-content p {
            margin: 0.5em 0;
            opacity: 0;
            animation: fadeIn 0.5s ease-in-out forwards;
          }
          
          .story-content p.fade-in {
            opacity: 1;
          }
          
          .cursor {
            display: inline-block;
            margin-left: 2px;
            color: #fff;
          }
          
          .blinking {
            animation: blink 0.7s infinite;
          }
          
          @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
          }
          
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
          
          @keyframes fadeOut {
            0% { opacity: 1; }
            100% { opacity: 0; visibility: hidden; }
          }
        `}</style>
      </div>
    </>
  );
}

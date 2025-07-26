'use client'
// 引入 React 相关钩子
import '../page_fonts.css';
import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import 'github-markdown-css/github-markdown.css'; 

// 白板便利贴风格的样式对象
const styles = {
    // 页面主容器样式 - 模拟墙面
    container: {
        display: 'flex', 
        flexDirection: 'column' as const, 
        alignItems: 'center', 
        justifyContent: 'flex-start', 
        minHeight: '100vh',
        padding: '24px',
        backgroundColor: '#f0f0e8',
        backgroundImage: 'linear-gradient(#e5e5e5 1px, transparent 1px), linear-gradient(90deg, #e5e5e5 1px, transparent 1px)',
        backgroundSize: '40px 40px',
        fontFamily: '"Marker Felt", "Comic Sans MS", cursive, sans-serif',
        position: 'relative',
        overflow: 'hidden',
    },
    // 白板容器
    chatBox: {
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#f5f5f5',
        borderRadius: '12px',
        boxShadow: 'inset 0 0 10px rgba(0,0,0,0.1)',
        overflow: 'hidden',
        maxWidth: '1200px',
        margin: '0 auto',
        width: '100%',
    },
    // 消息列表区域样式 - 垂直交替布局
    messages: {
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        padding: '20px',
        overflowY: 'auto',
        flex: 1,
        maxWidth: '800px',
        margin: '0 auto',
        width: '100%',
    },
    // 消息卡片基础样式
    messageCard: {
        padding: '24px',
        borderRadius: '12px',
        boxShadow: '3px 3px 8px rgba(0, 0, 0, 0.15)',
        position: 'relative',
        minHeight: '120px',
        maxWidth: '80%',
        width: 'fit-content',
        wordBreak: 'break-word',
        transition: 'all 0.3s ease',
        cursor: 'pointer',
        '&:hover': {
            transform: 'translateY(-3px) rotate(-1deg)',
            boxShadow: '5px 5px 12px rgba(0, 0, 0, 0.2)'
        },
        '&::before': {
            content: '""',
            position: 'absolute',
            top: '10px',
            right: '10px',
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: 'rgba(0,0,0,0.1)',
        }
    },
    // AI 消息卡片样式 - 黄色便利贴
    aiMsg: {
        background: '#f9f5e9',
        border: '1px solid #e0d5b8',
        margin: '15px 0',
        alignSelf: 'flex-start',
        marginRight: 'auto',
        marginLeft: '20px',
        fontSize: '20px', 
        '&:hover': {
            transform: 'rotate(-1deg)',
        },
        '&::after': {
            content: '""',
            position: 'absolute',
            bottom: '10px',
            right: '10px',
            fontSize: '12px',
            color: '#999',
        }
    },
    // 玩家消息卡片样式 - 蓝色便利贴
    playerMsg: {
        background: '#e3f2fd',
        border: '1px solid #bbdefb',
        margin: '15px 0',
        alignSelf: 'flex-end',
        marginLeft: 'auto',
        marginRight: '20px',
        fontSize: '20px', 
        '&:hover': {
            transform: 'rotate(1deg)',
        },
        '&::after': {
            content: '""',
            position: 'absolute',
            bottom: '10px',
            right: '10px',
            fontSize: '12px',
            color: '#999',
        }
    },
    // 输入区域容器
    inputArea: {
        display: 'flex',
        alignItems: 'center',
        background: 'white',
        borderRadius: '8px',
        border: '1px solid #d0c8b0',
        padding: '10px 15px',
        boxShadow: 'inset 0 1px 3px rgba(0, 0, 0, 0.1)',
        marginTop: 'auto',
    },
    // 输入框样式
    input: {
        flex: 1,
        border: 'none',
        outline: 'none',
        background: 'transparent',
        fontSize: '16px',
        fontFamily: '"Marker Felt", "Comic Sans MS", cursive, sans-serif',
        padding: '10px',
        color: '#333',
        '&::placeholder': {
            color: '#999',
            fontStyle: 'italic',
        }
    },
    // 发送按钮样式
    sendBtn: {
        marginLeft: '10px',
        background: '#4a90e2',
        color: 'white',
        border: 'none',
        borderRadius: '20px',
        padding: '8px 20px',
        fontSize: '16px',
        fontFamily: '"Marker Felt", "Comic Sans MS", cursive, sans-serif',
        cursor: 'pointer',
        boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
        transition: 'all 0.2s',
        '&:hover': {
            background: '#357abd',
            transform: 'translateY(-1px)',
        },
        '&:active': {
            transform: 'translateY(0)',
        }
    },
    // 装饰元素 - 图钉
    pin: {
        position: 'absolute',
        width: '10px',
        height: '10px',
        borderRadius: '50%',
        backgroundColor: '#c0c0c0',
        boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
        '&::after': {
            content: '""',
            position: 'absolute',
            top: '-5px',
            left: '2px',
            width: '6px',
            height: '10px',
            backgroundColor: '#e0e0e0',
            borderRadius: '50% 50% 0 0',
        }
    },
    // 标题样式
    title: {
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#333',
        marginBottom: '20px',
        textAlign: 'center',
        fontFamily: '"Permanent Marker", cursive',
        textShadow: '1px 1px 2px rgba(0,0,0,0.1)',
    }
};

// 消息类型定义
type Message = { role: 'ai' | 'player'; text: string };
// 初始消息，AI 欢迎语
const initialMessages: Message[] = [
    { 
        role: 'ai', 
        text: '1924年，马萨诸塞州，阿卡姆市。\n\n' +
              '窗外，连绵的秋雨不知疲倦地敲打着玻璃，将街道的煤气灯光晕染成一片模糊的昏黄。你正身处自己位于“德尔伍德古物研究会”三楼的办公室里。空气中弥漫着旧书、皮革与淡淡烟草混合的熟悉气味，唯一的声响来自角落里那座老式落地钟沉稳而规律的滴答声。\n\n' +
              '你的桌上摊着几份关于新英格兰地区乡野传说的手稿，其中一篇关于“蹲占者之湖”（Squatter Lake）的记述尤其让你在意——文中提到了怪异的乌鸦群和某些无法被点燃的木材。你正沉浸在这些尘封的记述中，试图将零散的线索拼凑成一个完整的图案。\n\n' +
              '就在这时——\n\n' +
              '笃，笃，笃。\n\n' +
              '三声清晰而有力的敲门声，穿透了雨声和钟摆声，打破了书房的宁静。这声音听起来既不匆忙，也不犹豫，带着一种不容拒绝的决断。\n\n' +
              '你的思绪被打断了。你会怎么做？' 
    },
];

// 等待特效组件：魔幻风格圆点跳动
const MagicTyping = () => (
  <>
    <span style={{ display: 'inline-block', minWidth: 48, verticalAlign: 'middle' }}>
      <span className="typing-dot" style={{ animationDelay: '0s' }} />
      <span className="typing-dot" style={{ animationDelay: '0.2s' }} />
      <span className="typing-dot" style={{ animationDelay: '0.4s' }} />
    </span>
    {/* 独立样式块 */}
    <style jsx>{`
      .typing-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        margin: 0 3px;
        background: #6a8a9a;
        border-radius: 50%;
        box-shadow: 0 0 8px #4a6a7a;
        animation: typing-bounce 1s infinite ease-in-out;
      }
      @keyframes typing-bounce {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.3; }
        40% { transform: translateY(-8px); opacity: 1; }
      }
    `}</style>
  </>
);

// 主页面组件
// 生成随机旋转角度
const getRandomRotation = () => (Math.random() * 6 - 3);

// 生成随机位置偏移
const getRandomOffset = () => (Math.random() * 20 - 10);

const Page = () => {
    // 消息列表状态
    const [messages, setMessages] = useState<Message[]>(initialMessages);
    // 输入框内容状态
    const [input, setInput] = useState('');
    // 用于滚动到底部的引用
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const [loading, setLoading] = useState(false);
    // 存储每个消息的随机旋转角度和偏移
    const [messageStyles, setMessageStyles] = useState<Array<{rotation: number, offset: number}>>([]);

    // 初始化消息样式
    useEffect(() => {
        setMessageStyles(messages.map(() => ({
            rotation: getRandomRotation(),
            offset: getRandomOffset()
        })));
    }, [messages.length]);

    // 每当消息更新时自动滚动到底部
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    // 发送消息处理函数
    const handleSend = async () => {
        if (!input.trim()) return;
        // 添加玩家消息到消息列表
        setMessages([...messages, { role: 'player', text: input }]);
        const userInput = input;
        setInput('');
        setLoading(true); // 开始等待
        try {
            // 向后端发送请求，获取 AI 回复
            const response = await fetch('http://127.0.0.1:8000/process-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: userInput }),
            });
            const data = await response.json();
            setLoading(false); // 结束等待
            if (data.output) {
                // 添加 AI 回复到消息列表
                setMessages(msgs => ([...msgs, { role: 'ai', text: data.output }]));
            } else if (data.error) {
                setMessages(msgs => ([...msgs, { role: 'ai', text: `后端返回错误: ${data.error}` }]));
            } else {
                setMessages(msgs => ([...msgs, { role: 'ai', text: '后端无有效响应' }]));
            }
        } catch (err) {
            setLoading(false); // 结束等待
            setMessages(msgs => ([...msgs, { role: 'ai', text: '无法连接到Python后端，请确认后端服务已启动。' }]));
        }
    };

    // 输入框回车发送消息
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div style={styles.container}>
            {/* 标题 */}
            <div style={{ 
                fontSize: 32, 
                fontWeight: 'bold', 
                margin: '0 0 32px 0',
                padding: '16px 40px',
                letterSpacing: 1.5, 
                color: '#4a4a4a',
                background: 'rgba(245, 245, 240, 0.85)',
                borderRadius: '8px',
                textAlign: 'center',
                boxShadow: '4px 4px 12px rgba(0,0,0,0.1), -2px -2px 8px rgba(255,255,255,0.8)',
                border: '1px solid rgba(0,0,0,0.08)',
                position: 'relative',
                overflow: 'hidden',
                fontFamily: '"Permanent Marker", cursive',
                textShadow: '1px 1px 2px rgba(0,0,0,0.1)'
            }}>
                <div style={{
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'linear-gradient(45deg, rgba(255,255,255,0.2) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.05) 75%, rgba(0,0,0,0.05))',
                    backgroundSize: '20px 20px',
                    opacity: 0.5,
                    pointerEvents: 'none'
                }} />
                <span style={{
                    position: 'relative',
                    zIndex: 1,
                    background: 'linear-gradient(90deg, #6a8a9a, #8a9aaa, #6a8a9a)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundSize: '200% auto',
                    animation: 'gradient 3s ease infinite'
                }}>
                    AllStory
                </span>
            </div>
            <style jsx global>{`
                @keyframes gradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
            `}</style>
            
            {/* 白板容器 */}
            <div style={styles.chatBox}>
                <h2 style={styles.title}>
                    调查白板
                    <span style={{
                        display: 'inline-block',
                        marginLeft: '10px',
                        fontSize: '14px',
                        fontWeight: 'normal',
                        color: '#666',
                        fontFamily: 'Comic Sans MS',
                    }}>
                        
                    </span>
                </h2>
                
                {/* 消息列表 - 网格布局 */}
                <div style={styles.messages}>
                    {messages.map((msg, idx) => {
                        // 将文本中的换行符转换为React元素
                        const formattedText = msg.text.split('\n').map((line, i, arr) => (
                            <React.Fragment key={i}>
                                {line}
                                {i < arr.length - 1 && <br />}
                            </React.Fragment>
                        ));
                        
                        // 获取当前消息的随机样式
                        const style = messageStyles[idx] || { rotation: 0, offset: 0 };
                        
                        return (
                            <div 
                                key={idx} 
                                className="message-card"
                                style={{
                                    ...styles.messageCard,
                                    ...(msg.role === 'ai' ? styles.aiMsg : styles.playerMsg),
                                    transform: `rotate(${messageStyles[idx]?.rotation || 0}deg) translate(${messageStyles[idx]?.offset || 0}px)`,
                                    transition: 'all 0.3s ease',
                                }}
                                onClick={() => {
                                    const newStyles = [...messageStyles];
                                    newStyles[idx] = {
                                        rotation: getRandomRotation(),
                                        offset: getRandomOffset()
                                    };
                                    setMessageStyles(newStyles);
                                }}
                            >
                                {/* 图钉装饰 */}
                                <div style={{
                                    ...styles.pin,
                                    top: '5px',
                                    left: '50%',
                                    transform: 'translateX(-50%)',
                                }} />
                                
                                {/* 消息内容 - 使用Markdown渲染 */}
                                <div className="markdown-body" style={{
                                    padding: '15px',
                                    fontSize: '20px',
                                    lineHeight: '1.9',
                                    color: '#333',
                                    backgroundColor: 'transparent',
                                }}>
                                    {msg.role === 'ai' ? (
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {msg.text}
                                        </ReactMarkdown>
                                    ) : (
                                        formattedText
                                    )}
                                </div>
                                
                                {/* 发送者标签 */}
                                <div style={{
                                    position: 'absolute',
                                    bottom: '5px',
                                    right: '10px',
                                    fontSize: '10px',
                                    color: '#999',
                                    fontStyle: 'italic',
                                }}>
                                    {msg.role === 'ai' ? 'AI' : '你'}
                                </div>
                            </div>
                        );
                    })}
                    
                    {/* 等待特效 */}
                    {loading && (
                        <div style={{
                            ...styles.messageCard,
                            ...styles.aiMsg,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            minHeight: '80px',
                        }}>
                            <MagicTyping />
                        </div>
                    )}
                    
                    {/* 滚动锚点 */}
                    <div ref={messagesEndRef} />
                </div>
                
                {/* 输入区域 */}
                <div style={styles.inputArea}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="写下你的线索或问题..."
                        style={styles.input}
                    />
                    <button 
                        onClick={handleSend} 
                        style={{
                            ...styles.sendBtn,
                            opacity: loading ? 0.7 : 1,
                            cursor: loading ? 'not-allowed' : 'pointer',
                        }}
                        disabled={loading}
                        onMouseDown={e => {
                            if (!loading) {
                                e.currentTarget.style.transform = 'translateY(2px)';
                                e.currentTarget.style.boxShadow = '0 1px 2px rgba(0,0,0,0.1)';
                            }
                        }}
                        onMouseUp={e => {
                            if (!loading) {
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
                            }
                        }}
                        onMouseLeave={e => {
                            if (!loading) {
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
                            }
                        }}
                    >
                        发送
                    </button>
                </div>
            </div>
            
            {/* 全局字体和样式 */}
            <style jsx global>{`
                @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Indie+Flower&family=Permanent+Marker&display=swap');
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                /* 自定义滚动条 */
                ::-webkit-scrollbar {
                    width: 8px;
                    height: 8px;
                }
                
                ::-webkit-scrollbar-track {
                    background: rgba(0, 0, 0, 0.05);
                    border-radius: 4px;
                }
                
                ::-webkit-scrollbar-thumb {
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 4px;
                }
                
                ::-webkit-scrollbar-thumb:hover {
                    background: rgba(0, 0, 0, 0.3);
                }
                
                /* 消息卡片动画 */
                .message-enter {
                    opacity: 0;
                    transform: scale(0.9);
                }
                
                .message-enter-active {
                    opacity: 1;
                    transform: scale(1);
                    transition: opacity 300ms, transform 300ms;
                }
            `}</style>
            
            {/* 全局Markdown样式 */}
            <style jsx global>{`
                .message-card .markdown-body {
                    font-family: inherit;
                    font-size: inherit;
                    line-height: 1.7;
                    padding: 0;
                    background-color: transparent;
                }
                .message-card .markdown-body pre {
                    background-color: rgba(0,0,0,0.05);
                    padding: 12px;
                    border-radius: 6px;
                    overflow-x: auto;
                }
                .message-card .markdown-body code {
                    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
                    padding: 0.2em 0.4em;
                    margin: 0;
                    font-size: 85%;
                    background-color: rgba(27,31,35,0.05);
                    border-radius: 3px;
                }
                .message-card .markdown-body pre code {
                    background-color: transparent;
                    padding: 0;
                    margin: 0;
                    font-size: 100%;
                    word-break: normal;
                    white-space: pre;
                    overflow: visible;
                }
                .message-card .markdown-body a {
                    color: #0366d6;
                    text-decoration: none;
                }
                .message-card .markdown-body a:hover {
                    text-decoration: underline;
                }
                .message-card .markdown-body blockquote {
                    border-left: 4px solid #dfe2e5;
                    color: #6a737d;
                    padding: 0 1em;
                    margin: 0.5em 0;
                }
                .message-card .markdown-body blockquote p {
                    margin: 0.5em 0;
                }
                .message-card .markdown-body table {
                    border-collapse: collapse;
                    width: 100%;
                    margin: 16px 0;
                }
                .message-card .markdown-body th,
                .message-card .markdown-body td {
                    border: 1px solid #dfe2e5;
                    padding: 6px 13px;
                    text-align: left;
                }
                .message-card .markdown-body tr {
                    background-color: #fff;
                    border-top: 1px solid #c6cbd1;
                }
                .message-card .markdown-body tr:nth-child(2n) {
                    background-color: #f6f8fa;
                }
            `}</style>
        </div>
    );
};

// 导出主页面组件
export default Page;
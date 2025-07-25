'use client'
// 引入 React 相关钩子
import React, { useState, useRef, useEffect } from 'react';

// 魔幻羊皮纸风格的简单内联样式对象
const styles = {
    // 页面主容器样式
    container: {
        display: 'flex', flexDirection: 'column' as const, alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#f5ecd6', fontFamily: 'serif',
    },
    // 聊天框样式
    chatBox: {
        width: '100%', maxWidth: 600, minHeight: 500, background: 'url("https://www.transparenttextures.com/patterns/old-mathematics.png") #f8f3e6',
        border: '4px solid #bfa76f', borderRadius: 24, boxShadow: '0 4px 24px #bfa76f55', padding: 24, marginBottom: 16,
        display: 'flex', flexDirection: 'column' as const, justifyContent: 'flex-end',
    },
    // 消息列表区域样式
    messages: {
        flex: 1, overflowY: 'auto' as const, marginBottom: 16,
    },
    // AI 消息气泡样式
    aiMsg: {
        alignSelf: 'flex-start', background: 'rgba(255,255,240,0.95)', color: '#2d2d2d', borderRadius: '18px 18px 18px 6px', padding: '12px 18px', margin: '8px 0', fontFamily: 'cursive', boxShadow: '0 2px 8px #bfa76f33', border: '1.5px solid #bfa76f',
    },
    // 玩家消息气泡样式
    playerMsg: {
        alignSelf: 'flex-end', background: 'rgba(240,235,220,0.95)', color: '#3a2c1a', borderRadius: '18px 18px 6px 18px', padding: '12px 18px', margin: '8px 0', fontFamily: 'serif', boxShadow: '0 2px 8px #bfa76f22', border: '1.5px solid #bfa76f',
    },
    // 输入区域样式
    inputArea: {
        display: 'flex', alignItems: 'center', background: 'url("https://www.transparenttextures.com/patterns/old-mathematics.png") #f8f3e6', borderRadius: 16, border: '2px solid #bfa76f', padding: '8px 12px',
    },
    // 输入框样式
    input: {
        flex: 1, border: 'none', outline: 'none', background: 'rgba(255,255,240,0.95)', fontSize: 18, fontFamily: 'serif', padding: '8px', color: '#3a2c1a',
    },
    // 发送按钮样式
    sendBtn: {
        marginLeft: 12, background: '#bfa76f', color: '#fff', border: 'none', borderRadius: 12, padding: '8px 18px', fontSize: 18, fontFamily: 'fantasy', cursor: 'pointer', boxShadow: '0 2px 8px #bfa76f55', transition: 'background 0.2s',
    },
    // 羽毛图标样式
    feather: {
        width: 28, height: 28, marginRight: 8,
    }
};

// 羽毛 SVG 图标
const featherSvg = (
    <svg style={styles.feather} viewBox="0 0 32 32" fill="none"><path d="M4 28C4 28 28 4 28 4M4 28C4 28 12 24 16 20M4 28C4 28 8 20 20 8" stroke="#bfa76f" strokeWidth="2.5" strokeLinecap="round" /></svg>
);

// 消息类型定义
type Message = { role: 'ai' | 'player'; text: string };
// 初始消息，AI 欢迎语
const initialMessages: Message[] = [
    { role: 'ai', text: '欢迎来到AI地下城主的世界，勇敢的冒险者！你准备好开始冒险了吗？' },
];

// 主页面组件
const Page = () => {
    // 消息列表状态
    const [messages, setMessages] = useState<Message[]>(initialMessages);
    // 输入框内容状态
    const [input, setInput] = useState('');
    // 用于滚动到底部的引用
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

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
        try {
            // 向后端发送请求，获取 AI 回复
            const response = await fetch('http://127.0.0.1:8000/process-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: userInput }),
            });
            const data = await response.json();
            if (data.output) {
                // 添加 AI 回复到消息列表
                setMessages(msgs => ([...msgs, { role: 'ai', text: data.output }]));
            } else if (data.error) {
                setMessages(msgs => ([...msgs, { role: 'ai', text: `后端返回错误: ${data.error}` }]));
            } else {
                setMessages(msgs => ([...msgs, { role: 'ai', text: '后端无有效响应' }]));
            }
        } catch (err) {
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
            <div style={{ fontSize: 32, fontWeight: 'bold', marginBottom: 24, letterSpacing: 2, color: '#bfa76f', textShadow: '0 2px 8px #bfa76f55' }}>
                AI地下城主
            </div>
            {/* 聊天框 */}
            <div style={styles.chatBox}>
                {/* 消息列表 */}
                <div style={styles.messages}>
                    {messages.map((msg, idx) => (
                        <div key={idx} style={msg.role === 'ai' ? styles.aiMsg : styles.playerMsg}>
                            {msg.text}
                        </div>
                    ))}
                    {/* 滚动锚点 */}
                    <div ref={messagesEndRef} />
                </div>
                {/* 输入区域 */}
                <div style={styles.inputArea}>
                    {featherSvg}
                    <input
                        style={styles.input}
                        type="text"
                        placeholder="在此输入你的行动..."
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                    <button style={styles.sendBtn} onClick={handleSend}>
                        发送
                    </button>
                </div>
            </div>
        </div>
    );
};

// 导出主页面组件
export default Page;
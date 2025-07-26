'use client'
// 引入 React 相关钩子
import React, { useState, useRef, useEffect } from 'react';

// 魔幻羊皮纸风格的简单内联样式对象
const styles = {
    // 页面主容器样式
    container: {
        display: 'flex', flexDirection: 'column' as const, alignItems: 'center', justifyContent: 'center', minHeight: '100vh', 
        background: 'linear-gradient(180deg, #0a1a2a 0%, #1a3a4a 50%, #0d2b3a 100%)', 
        fontFamily: 'serif',
    },
    // 聊天框样式
    chatBox: {
        width: '100%', maxWidth: 600, minHeight: 500, 
        background: 'linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%)',
        border: '4px solid #2a4a5a', borderRadius: 24, 
        boxShadow: '0 4px 24px #0008, inset 0 1px 2px #4a6a7a', 
        padding: 24, marginBottom: 16,
        display: 'flex', flexDirection: 'column' as const, justifyContent: 'flex-end',
    },
    // 消息列表区域样式
    messages: {
        flex: 1, overflowY: 'auto' as const, marginBottom: 16,
    },
    // AI 消息气泡样式
    aiMsg: {
        alignSelf: 'flex-start', 
        background: 'linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%)', 
        color: '#8ba3b3', 
        borderRadius: '18px 18px 18px 6px', 
        padding: '12px 18px', 
        margin: '8px 0', 
        fontFamily: 'serif', 
        boxShadow: '0 2px 8px #0004, inset 0 1px 2px #4a6a7a', 
        border: '2px solid #2a4a5a',
        textShadow: '0 0 4px #4a6a7a',
    },
    // 玩家消息气泡样式
    playerMsg: {
        alignSelf: 'flex-end', 
        background: 'linear-gradient(135deg, #2a3a4a 0%, #3a4a5a 100%)', 
        color: '#9ba3b3', 
        borderRadius: '18px 18px 6px 18px', 
        padding: '12px 18px', 
        margin: '8px 0', 
        fontFamily: 'serif', 
        boxShadow: '0 2px 8px #0004, inset 0 1px 2px #5a7a8a', 
        border: '2px solid #3a5a6a',
        textShadow: '0 0 4px #5a7a8a',
    },
    // 输入区域样式
    inputArea: {
        display: 'flex', alignItems: 'center', 
        background: 'linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%)', 
        borderRadius: 16, 
        border: '2px solid #2a4a5a', 
        padding: '8px 12px',
        boxShadow: '0 2px 8px #0004, inset 0 1px 2px #4a6a7a',
    },
    // 输入框样式
    input: {
        flex: 1, border: 'none', outline: 'none', 
        background: 'linear-gradient(135deg, #2a3a4a 0%, #3a4a5a 100%)', 
        fontSize: 18, fontFamily: 'serif', padding: '8px', 
        color: '#8ba3b3',
        borderRadius: 8,
        boxShadow: 'inset 0 1px 2px #4a6a7a',
        textShadow: '0 0 2px #4a6a7a',
    },
    // 发送按钮样式
    sendBtn: {
        marginLeft: 12, 
        background: 'linear-gradient(135deg, #2a4a5a 0%, #3a5a6a 100%)', 
        color: '#8ba3b3', 
        border: '3px solid #2a4a5a', 
        borderRadius: 12, 
        padding: '8px 18px', 
        fontSize: 18, 
        fontFamily: 'serif', 
        cursor: 'pointer', 
        boxShadow: '0 2px 8px #0004, inset 0 1px 2px #4a6a7a', 
        transition: 'box-shadow 0.2s, border 0.2s, transform 0.2s',
        textShadow: '0 0 4px #4a6a7a',
    },
    // 羽毛图标样式
    feather: {
        width: 28, height: 28, marginRight: 8,
        filter: 'brightness(0.7) contrast(1.2) hue-rotate(180deg)',
    }
};

// 羽毛 SVG 图标
const featherSvg = (
    <svg style={styles.feather} viewBox="0 0 32 32" fill="none"><path d="M4 28C4 28 28 4 28 4M4 28C4 28 12 24 16 20M4 28C4 28 8 20 20 8" stroke="#bfa76f" strokeWidth="2.5" strokeLinecap="round"/></svg>
);

// 消息类型定义
type Message = { role: 'ai' | 'player'; text: string };
// 初始消息，AI 欢迎语
const initialMessages: Message[] = [
    { role: 'ai', text: '准备好探寻真相了吗...' },
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
const Page = () => {
    // 消息列表状态
    const [messages, setMessages] = useState<Message[]>(initialMessages);
    // 输入框内容状态
    const [input, setInput] = useState('');
    // 用于滚动到底部的引用
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const [loading, setLoading] = useState(false);

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
                marginBottom: 24, 
                letterSpacing: 2, 
                color: '#6a8a9a', 
                textShadow: '0 0 16px #4a6a7a, 0 2px 8px #000',
                background: 'linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%)',
                borderRadius: 12,
                padding: '8px 24px',
                border: '2px solid #2a4a5a',
                boxShadow: '0 4px 16px #0004, inset 0 1px 2px #4a6a7a',
            }}>
                Game Agent
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
                    {/* 等待特效 */}
                    {loading && (
                        <div style={{ display: 'flex', alignItems: 'center', minHeight: 32, margin: '8px 0 0 0' }}>
                            <MagicTyping />
                        </div>
                    )}
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
                    <button
                        style={styles.sendBtn}
                        onClick={handleSend}
                        onMouseDown={e => {
                            e.currentTarget.style.transform = 'translateY(2px) scale(0.97)';
                            e.currentTarget.style.border = '3px solid #4a6a7a';
                            e.currentTarget.style.boxShadow = '0 1px 4px #0004, inset 0 1px 2px #6a8a9a';
                        }}
                        onMouseUp={e => {
                            e.currentTarget.style.transform = 'translateY(-3px) scale(1.03)';
                            e.currentTarget.style.border = '3px solid #4a6a7a';
                            e.currentTarget.style.boxShadow = '0 4px 16px #0006, inset 0 1px 2px #6a8a9a, 0 0 8px #4a6a7a';
                        }}
                        onMouseLeave={e => {
                            e.currentTarget.style.transform = 'none';
                            e.currentTarget.style.border = '3px solid #2a4a5a';
                            e.currentTarget.style.boxShadow = '0 2px 8px #0004, inset 0 1px 2px #4a6a7a';
                        }}
                        onMouseOver={e => {
                            e.currentTarget.style.transform = 'translateY(-3px) scale(1.03)';
                            e.currentTarget.style.border = '3px solid #4a6a7a';
                            e.currentTarget.style.boxShadow = '0 4px 16px #0006, inset 0 1px 2px #6a8a9a, 0 0 8px #4a6a7a';
                        }}
                    >
                        发送
                    </button>
                </div>
            </div>
        </div>
    );
};

// 导出主页面组件
export default Page;

/* 在文件底部追加动画样式 */
<style jsx global>{`
@keyframes magic-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 1; }
  40% { transform: translateY(-10px); opacity: 0.7; }
}`}</style>
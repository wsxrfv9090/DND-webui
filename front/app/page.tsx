'use client';
// 引入 Next.js 的图片组件
import Image from "next/image";
// 引入 Next.js 的路由钩子，用于页面跳转
import { useRouter } from "next/navigation";

export default function Home() {
  // 获取路由对象，用于页面跳转
  const router = useRouter();
  return (
    // 页面主容器，设置背景和布局
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #23211a 60%, #3a3322 100%)', display: 'flex', flexDirection: 'column' }}>
      {/* 页眉部分，显示标题 */}
      <header style={{ width: '100%', padding: '32px 0 16px 0', textAlign: 'center', background: 'rgba(40, 36, 24, 0.92)', fontFamily: 'serif', fontSize: 36, fontWeight: 'bold', letterSpacing: 4, borderBottom: '3px solid #7a5c1e', boxShadow: '0 2px 8px #000a', color: '#d6cfa3', textShadow: '0 2px 8px #000a' }}>
        {/* 标题左侧有地球图标背景 */}
        <span style={{ background: 'url(/globe.svg) left center/40px no-repeat', paddingLeft: 48 }}>角色创建</span>
      </header>
      {/* 主体内容区域 */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'row', maxWidth: 700, margin: '40px auto', width: '100%', gap: 0 }}>
        {/* 左侧角色信息填写区 */}
        <section style={{ flex: 1, background: 'rgba(36,32,24,0.92)', borderRadius: 18, boxShadow: '0 2px 18px #000b', padding: 40, display: 'flex', flexDirection: 'column', gap: 36, border: '2.5px solid #7a5c1e', minWidth: 340, color: '#d6cfa3', fontFamily: 'serif', position: 'relative' }}>
          {/* 古旧卷轴边角装饰 */}
          <div style={{ position: 'absolute', left: -18, top: -18, width: 36, height: 36, background: 'url(/window.svg) center/contain no-repeat', opacity: 0.25 }} />
          <div style={{ position: 'absolute', right: -18, bottom: -18, width: 36, height: 36, background: 'url(/vercel.svg) center/contain no-repeat', opacity: 0.25 }} />
          {/* 基本信息填写表单 */}
          <div style={{ marginBottom: 24 }}>
            <h2 style={{ fontFamily: 'serif', fontSize: 24, marginBottom: 16, color: '#bfa76a', textShadow: '0 1px 4px #000a' }}>基本信息</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {/* 姓名输入框 */}
              <label>姓名 <input type="text" placeholder="请输入角色姓名" style={{ marginLeft: 8, padding: 4, borderRadius: 4, border: '1.5px solid #7a5c1e', background: '#23211a', color: '#e7e2c0', fontFamily: 'serif' }} /></label>
              {/* 种族选择框 */}
              <label>种族 <select style={{ marginLeft: 8, padding: 4, borderRadius: 4, border: '1.5px solid #7a5c1e', background: '#23211a', color: '#e7e2c0', fontFamily: 'serif' }}><option>人类</option><option>精灵</option><option>矮人</option><option>半身人</option></select></label>
              {/* 职业选择框 */}
              <label>职业 <select style={{ marginLeft: 8, padding: 4, borderRadius: 4, border: '1.5px solid #7a5c1e', background: '#23211a', color: '#e7e2c0', fontFamily: 'serif' }}><option>战士</option><option>法师</option><option>游侠</option><option>牧师</option></select></label>
              {/* 背景输入框 */}
              <label>背景 <input type="text" placeholder="如：流浪者、学者" style={{ marginLeft: 8, padding: 4, borderRadius: 4, border: '1.5px solid #7a5c1e', background: '#23211a', color: '#e7e2c0', fontFamily: 'serif' }} /></label>
            </div>
          </div>
          {/* 属性分配区 */}
          <div>
            <h2 style={{ fontFamily: 'serif', fontSize: 24, marginBottom: 16, color: '#bfa76a', textShadow: '0 1px 4px #000a' }}>属性分配</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {/* 六项属性分配，每项有加减按钮和当前值（此处未实现交互，仅为静态展示） */}
              {['力量', '敏捷', '体质', '智力', '感知', '魅力'].map(attr => (
                <div key={attr} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span style={{ width: 48 }}>{attr}</span>
                  <button style={{ width: 28, height: 28, borderRadius: 6, border: '1.5px solid #7a5c1e', background: '#3a3322', color: '#bfa76a', fontWeight: 'bold', fontFamily: 'serif', boxShadow: '0 1px 2px #000a' }}>-</button>
                  <span style={{ width: 32, textAlign: 'center', fontWeight: 'bold', fontSize: 18 }}>{10}</span>
                  <button style={{ width: 28, height: 28, borderRadius: 6, border: '1.5px solid #7a5c1e', background: '#3a3322', color: '#bfa76a', fontWeight: 'bold', fontFamily: 'serif', boxShadow: '0 1px 2px #000a' }}>+</button>
                </div>
              ))}
              {/* 剩余可分配点数（静态展示） */}
              <div style={{ marginTop: 12, color: '#bfa76a', fontWeight: 'bold', textShadow: '0 1px 2px #000a' }}>剩余可分配点数: <span>0</span></div>
            </div>
          </div>
        </section>
      </main>
      {/* 页脚，包含操作按钮 */}
      <footer style={{ width: '100%', padding: '20px 0', background: 'linear-gradient(90deg,#23211a 0%,#3a3322 100%)', borderTop: '3px solid #7a5c1e', display: 'flex', justifyContent: 'center', gap: 32, fontFamily: 'serif', fontSize: 20, fontWeight: 'bold', boxShadow: '0 -2px 8px #000a' }}>
        {/* 完成创建按钮，点击跳转到 AIchatcoc 页面 */}
        <button
          style={{ padding: '10px 32px', borderRadius: 8, border: '2px solid #7a5c1e', background: '#3a3322', color: '#bfa76a', fontWeight: 'bold', fontSize: 20, marginRight: 16, boxShadow: '0 1px 2px #000a' }}
          onClick={() => router.push('/AIchatcoc')}
        >
          完成创建
        </button>
        {/* 重置按钮（未实现功能，仅样式） */}
        <button style={{ padding: '10px 32px', borderRadius: 8, border: '2px solid #7a5c1e', background: '#23211a', color: '#bfa76a', fontWeight: 'bold', fontSize: 20, boxShadow: '0 1px 2px #000a' }}>重置</button>
      </footer>
    </div>
  );
}

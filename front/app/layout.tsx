// 引入 Google 字体
import { Geist, Geist_Mono } from "next/font/google";
// 引入全局样式
import "./globals.css";

// 配置 Geist Sans 字体变量
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});
// 配置 Geist Mono 字体变量
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// 全局元数据设置
export const metadata = {
  title: "DND-webui",
  description: "DND-webui",
};

// 根布局组件，包裹所有页面内容
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* 渲染所有子页面内容 */}
        {children}
      </body>
    </html>
  );
}

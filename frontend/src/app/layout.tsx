import type { Metadata } from "next";
import { Inter} from "next/font/google";
import "./globals.scss";
import {Toaster} from 'sonner'

const inter = Inter({subsets: ["latin"]})

export const metadata: Metadata = {
  title: "Cardapio Digital",
  description: "Uma forma prática de organizar os pedidos!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br">
      <body className={inter.className}>
        <Toaster
          position="bottom-right"
          toastOptions={{
            style:{
              backgroundColor: "#f1f1f1",
              color: "#131313",
              borderColor: "rgba(255,255,255,0.5"
            }
          }}
        />
        {children}
      </body>
    </html>
  );
}

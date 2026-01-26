import '../../styles/globals.css';
import type { AppProps } from 'next/app';
import { UserProvider } from '../context/UserContext';
import { Inter, Outfit } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' });

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <UserProvider>
      <main className={`${inter.variable} ${outfit.variable} font-sans`}>
        <Component {...pageProps} />
      </main>
    </UserProvider>
  );
}
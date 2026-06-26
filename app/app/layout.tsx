import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DolphiSIC Redesign',
  description: 'Gestion du parc radio et cartographie opérationnelle du SDIS 04',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fr" className="dark">
      <body>{children}</body>
    </html>
  );
}



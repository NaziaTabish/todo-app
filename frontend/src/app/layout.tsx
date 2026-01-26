/** Root layout for Todo application */

import { UserProvider } from '../context/UserContext';
import '../../styles/globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <UserProvider>
          <div id="root">{children}</div>
        </UserProvider>
      </body>
    </html>
  );
}
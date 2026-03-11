"use client";

import { usePathname } from "next/navigation";
import { useAuth } from "./AuthProvider";
import Shell from "./Shell";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const pathname = usePathname();

  // Don't show Shell on login page
  if (pathname === "/login" || !user) {
    return <>{children}</>;
  }

  return <Shell>{children}</Shell>;
}

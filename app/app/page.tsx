'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import Menu, { type IMenu } from '@/components/ui/navbar';

declare global {
  interface Window {
    onLegacyViewChanged?: (viewId: string) => void;
    onLegacyNavigationSettingsChanged?: (enabled: boolean) => void;
  }
}

const NAV_COLLAPSED_KEY = 'dolphisic_nav_collapsed';
const NAV_AUTO_COLLAPSE_KEY = 'dolphisic_nav_auto_collapse';

const menus: IMenu[] = [
  { id: 1, title: 'Tableau de bord', url: '#dashboard' },
  {
    id: 2,
    title: 'Parc matériel',
    url: '#standard',
    dropdown: true,
    items: [
      { id: 21, title: 'Vue Standard', url: '#standard' },
      { id: 22, title: 'Recherche Avancée', url: '#search' },
      { id: 23, title: 'Statistiques', url: '#stats' },
    ],
  },
  { id: 3, title: 'Cartographie', url: '#carto' },
  { id: 4, title: 'Stock SDIS04', url: '#stock' },
  { id: 6, title: 'Notifications', url: '#notifications' },
  { id: 5, title: 'Paramètres', url: '#settings' },
];

const viewIds: Record<string, string> = {
  '#dashboard': 'dashboard',
  '#standard': 'standard',
  '#search': 'search',
  '#stats': 'stats',
  '#carto': 'carto',
  '#stock': 'stock',
  '#notifications': 'notifications',
  '#settings': 'settings',
};

const viewLabels: Record<string, string> = {
  '#dashboard': 'Tableau de bord',
  '#standard': 'Vue Standard',
  '#search': 'Recherche Avancée',
  '#stats': 'Statistiques',
  '#carto': 'Cartographie',
  '#stock': 'Stock SDIS04',
  '#notifications': 'Notifications',
  '#settings': 'Paramètres',
};

export default function Home() {
  const frameRef = useRef<HTMLIFrameElement>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeTab, setActiveTab] = useState('#dashboard');
  const [isNavCollapsed, setIsNavCollapsed] = useState(false);
  const [autoCollapse, setAutoCollapse] = useState(false);
  const lastAppliedTab = useRef('');

  const updateNavCollapsed = useCallback((collapsed: boolean, persist = true) => {
    setIsNavCollapsed(collapsed);
    if (persist) localStorage.setItem(NAV_COLLAPSED_KEY, collapsed ? '1' : '0');
  }, []);

  useEffect(() => {
    const applyAutoCollapse = (enabled: boolean) => {
      setAutoCollapse(enabled);
      updateNavCollapsed(enabled, !enabled);
    };

    const savedAutoCollapse = localStorage.getItem(NAV_AUTO_COLLAPSE_KEY) === '1';
    setAutoCollapse(savedAutoCollapse);
    setIsNavCollapsed(savedAutoCollapse || localStorage.getItem(NAV_COLLAPSED_KEY) === '1');

    window.onLegacyNavigationSettingsChanged = applyAutoCollapse;
    const handleStorage = (event: StorageEvent) => {
      if (event.key === NAV_AUTO_COLLAPSE_KEY) applyAutoCollapse(event.newValue === '1');
    };
    window.addEventListener('storage', handleStorage);

    return () => {
      delete window.onLegacyNavigationSettingsChanged;
      window.removeEventListener('storage', handleStorage);
    };
  }, [updateNavCollapsed]);

  useEffect(() => {
    window.onLegacyViewChanged = (viewId: string) => {
      const matchingTab = Object.entries(viewIds).find(([, id]) => id === viewId)?.[0];
      if (!matchingTab) return;

      lastAppliedTab.current = matchingTab;
      setActiveTab(matchingTab);
    };

    return () => {
      delete window.onLegacyViewChanged;
    };
  }, []);

  const handleTabChange = useCallback((tabUrl: string) => {
    setActiveTab(tabUrl);
  }, []);

  const [iframeSettled, setIframeSettled] = useState(false);

  const checkLoginState = useCallback(() => {
    if (typeof window === 'undefined') return;

    const token = localStorage.getItem('cryptis_token') || sessionStorage.getItem('cryptis_token');

    // No token → not logged in
    if (!token) {
      setIsLoggedIn(false);
      return;
    }

    // Token exists – check if iframe is still showing the login form
    try {
      const doc = frameRef.current?.contentDocument;
      if (doc) {
        const hasLoginForm =
          doc.querySelector('input[type="password"]') !== null ||
          Array.from(doc.querySelectorAll('button')).some(btn => {
            const text = (btn.textContent || '').trim().toLowerCase();
            return text.includes("s'authentifier");
          });
        if (hasLoginForm) {
          // Login form visible → don't show navbar (but do NOT remove the token!)
          setIsLoggedIn(false);
          return;
        }
      }
    } catch {
      // cross-origin – ignore
    }

    // Token exists and no login form visible → logged in
    setIsLoggedIn(true);
  }, []);

  // Only start polling AFTER the iframe has settled (React inside needs time to read
  // localStorage via useEffect and re-render from login-form → dashboard)
  useEffect(() => {
    if (!iframeSettled) return;
    checkLoginState();
    const interval = setInterval(checkLoginState, 500);
    return () => clearInterval(interval);
  }, [iframeSettled, checkLoginState]);

  const navigateIframe = useCallback((tabUrl: string) => {
    try {
      const documentFrame = frameRef.current?.contentDocument;
      const iframeWindow = frameRef.current?.contentWindow as any;
      if (!documentFrame || !iframeWindow) return;
      if (lastAppliedTab.current === tabUrl) return;

      const viewId = viewIds[tabUrl] || 'dashboard';

      // 1. Direct call to the IIFE-injected global switcher inside the legacy frame
      if (iframeWindow && typeof iframeWindow.changeLegacyView === 'function') {
        iframeWindow.changeLegacyView(viewId);
        lastAppliedTab.current = tabUrl;
        return;
      }

      // 2. Direct call fallback to the state setter
      if (iframeWindow && typeof iframeWindow.setLegacyPage === 'function' && viewId !== 'dashboard' && viewId !== 'settings' && viewId !== 'notifications') {
        iframeWindow.setLegacyPage(viewId);
        lastAppliedTab.current = tabUrl;
        return;
      }

      // 3. Button click fallback (queries DOM button elements and click)
      const label = viewLabels[tabUrl] || viewLabels['#dashboard'];
      const target = Array.from(documentFrame.querySelectorAll('button')).find((button) => {
        const text = (button.textContent || '').trim();
        const title = (button.getAttribute('title') || '').trim();
        return text.includes(label) || title.includes(label);
      });

      if (target instanceof HTMLButtonElement) {
        target.click();
        lastAppliedTab.current = tabUrl;
      }
    } catch (error) {
      console.error("Error navigating legacy iframe:", error);
    }
  }, []);

  // Sync activeTab state with legacy iframe (on changes and using a polling interval to catch updates/reloads)
  useEffect(() => {
    if (!isLoggedIn) return;
    navigateIframe(activeTab);
    const interval = setInterval(() => {
      navigateIframe(activeTab);
    }, 400);
    return () => clearInterval(interval);
  }, [isLoggedIn, activeTab, navigateIframe]);

  return (
    <main className={isLoggedIn ? `redesign-shell ${isNavCollapsed ? 'redesign-shell-nav-collapsed' : ''}` : "w-screen h-screen"}>
      {isLoggedIn && (
        <>
        {autoCollapse && isNavCollapsed && (
          <div
            className="redesign-nav-reveal-zone"
            onMouseEnter={() => setIsNavCollapsed(false)}
            aria-hidden="true"
          />
        )}
        <header
          className={`redesign-header relative z-50 flex min-w-0 items-center justify-center border-b border-border bg-background px-4 shadow-lg lg:px-6 ${isNavCollapsed ? 'redesign-header-collapsed' : ''}`}
          onMouseEnter={() => {
            if (autoCollapse) setIsNavCollapsed(false);
          }}
          onMouseLeave={() => {
            if (autoCollapse) setIsNavCollapsed(true);
          }}
        >
          <div className="absolute left-4 flex shrink-0 items-center gap-3 lg:left-6">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/logo-BXvTnzfG.png" alt="DolphiSIC" className="h-10 w-10 object-contain" />
            <strong className="hidden text-base font-extrabold tracking-wide sm:block">DolphiSIC</strong>
          </div>
          <div className="redesign-nav-panel">
            <Menu list={menus} activeTab={activeTab} onTabChange={handleTabChange} />
          </div>
          {!autoCollapse && (
            <button
              type="button"
              className={`redesign-nav-toggle ${isNavCollapsed ? 'redesign-nav-toggle-collapsed' : ''}`}
              onClick={() => updateNavCollapsed(!isNavCollapsed)}
              aria-label={isNavCollapsed ? 'Déployer la navigation' : 'Rétracter la navigation'}
              title={isNavCollapsed ? 'Déployer la navigation' : 'Rétracter la navigation'}
            >
              {isNavCollapsed ? <ChevronDown aria-hidden="true" /> : <ChevronUp aria-hidden="true" />}
            </button>
          )}
        </header>
        </>
      )}
      <iframe
        ref={frameRef}
        title="Application DolphiSIC"
        src="/legacy/index.html?redesign=1"
        className="redesign-frame"
        onLoad={() => {
          lastAppliedTab.current = '';
          // Give the React app inside 1.5s to read localStorage and re-render
          setTimeout(() => {
            setIframeSettled(true);
            navigateIframe(activeTab);
          }, 1500);
        }}
      />
    </main>
  );
}

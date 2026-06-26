'use client';

import Link from 'next/link';
import { useState } from 'react';
import { motion, MotionConfig } from 'framer-motion';
import * as React from 'react';

export type IMenu = {
  id: number;
  title: string;
  url: string;
  dropdown?: boolean;
  items?: IMenu[];
};

type MenuProps = {
  list: IMenu[];
  activeTab?: string;
  onTabChange?: (url: string) => void;
};

const isTabActive = (item: IMenu, activeTab: string) => {
  if (item.url === activeTab) return true;
  if (item.dropdown && item.items) {
    return item.items.some((sub) => sub.url === activeTab);
  }
  return false;
};

const Menu = ({ list, activeTab, onTabChange }: MenuProps) => {
  const [hovered, setHovered] = useState<number | null>(null);

  return (
    <MotionConfig transition={{ bounce: 0, type: 'tween' }}>
      <nav className="relative min-w-0" aria-label="Navigation principale">
        <ul className="flex items-center justify-center whitespace-nowrap">
          {list?.map((item) => {
            const isActive = isTabActive(item, activeTab || '');
            return (
              <li
                key={item.id}
                className="relative"
                onMouseEnter={() => setHovered(item.id)}
                onMouseLeave={() => setHovered(null)}
              >
                <Link
                  className={`
                    relative flex items-center justify-center rounded px-6 py-3 text-sm font-semibold transition-all
                    hover:bg-foreground/10
                    ${hovered === item?.id || isActive ? 'bg-foreground/10' : ''}
                  `}
                  href={item?.url}
                  onClick={(e) => {
                    e.preventDefault();
                    onTabChange?.(item?.url);
                  }}
                >
                  {item?.title}
                </Link>
                {(hovered === item?.id || isActive) && (
                  <motion.div
                    layout
                    layoutId="cursor"
                    className="absolute bottom-0 left-0 h-0.5 w-full bg-primary"
                  />
                )}
                {item?.dropdown && hovered === item?.id && (
                  <div className="absolute left-0 top-full z-50 pt-3">
                    <motion.div
                      layout
                      transition={{ bounce: 0 }}
                      initial={{ y: 10 }}
                      animate={{ y: 0 }}
                      exit={{ y: 10 }}
                      style={{ borderRadius: '8px' }}
                      className="flex w-64 flex-col overflow-hidden rounded border border-border bg-background shadow-2xl"
                    >
                      {item?.items?.map((nav) => {
                        const isSubActive = activeTab === nav.url;
                        return (
                          <motion.a
                            key={`link-${nav?.id}`}
                            href={`${nav?.url}`}
                            onClick={(e) => {
                              e.preventDefault();
                              onTabChange?.(nav?.url);
                            }}
                            className={`w-full p-4 text-sm font-medium hover:bg-muted transition-colors ${
                              isSubActive ? 'bg-muted text-primary' : ''
                            }`}
                          >
                            {nav?.title}
                          </motion.a>
                        );
                      })}
                    </motion.div>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </nav>
    </MotionConfig>
  );
};

export default Menu;


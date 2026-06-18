import React from "react";

interface MagicCardProps extends React.HTMLAttributes<HTMLDivElement> {
  gradientColor?: string;
  gradientSize?: number;
  gradientOpacity?: number;
}

export function MagicCard({
  children,
  className = "",
  gradientColor: _gradientColor,
  gradientSize: _gradientSize,
  gradientOpacity: _gradientOpacity,
  ...props
}: MagicCardProps) {
  return (
    <div
      className={`relative overflow-hidden rounded-xl border border-slate-800 bg-slate-900 text-slate-100 ${className}`}
      {...props}
    >
      <div className="relative z-10">{children}</div>
    </div>
  );
}

import React from "react";

interface PulsatingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  pulseColor?: string;
  duration?: string;
  distance?: string;
}

export function PulsatingButton({
  children,
  className = "",
  pulseColor = "#3b82f6",
  duration = "1.5s",
  distance = "8px",
  ...props
}: PulsatingButtonProps) {
  const pulseStyle = {
    "--pulse-color": pulseColor + "66", // 40% opacity
    "--pulse-color-fade": pulseColor + "00", // 0% opacity
    "--pulse-distance": distance,
    "--duration": duration,
    "backgroundColor": pulseColor,
  } as React.CSSProperties;

  return (
    <button
      className={`relative text-white font-semibold py-2.5 px-5 rounded-lg hover:brightness-110 active:scale-95 transition-all animate-pulse focus:outline-none z-10 ${className}`}
      style={pulseStyle}
      {...props}
    >
      <span className="relative z-10">{children}</span>
    </button>
  );
}

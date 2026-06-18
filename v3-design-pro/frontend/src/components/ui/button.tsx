import React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export function Button({ className = "", children, ...props }: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:pointer-events-none disabled:opacity-50 bg-blue-600 text-white hover:bg-blue-700 active:scale-98 h-10 px-4 py-2 w-full ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

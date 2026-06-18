import React from "react";

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {}

export function Label({ className = "", children, ...props }: LabelProps) {
  return (
    <label
      className={`text-sm font-semibold font-mono text-slate-300 leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 ${className}`}
      {...props}
    >
      {children}
    </label>
  );
}

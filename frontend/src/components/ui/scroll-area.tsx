import React from 'react';
import { cn } from '../../lib/utils';

interface ScrollAreaProps {
  className?: string;
  children: React.ReactNode;
}

export function ScrollArea({ className, children, ...props }: ScrollAreaProps) {
  return (
    <div
      className={cn("relative overflow-auto", className)}
      {...props}
    >
      {children}
    </div>
  );
}

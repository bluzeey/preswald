import React from "react";
import { cn } from "@/lib/utils";

const MatplotlibPlotWidget = ({ id, data, className, onError }) => {
  // Check if image data exists
  if (!data || !data.image) {
    return (
      <div className={cn("p-4 text-red-500", className)}>
        No plot data available
      </div>
    );
  }

  return (
    <div
      id={id}
      className={cn(
        "flex justify-center items-center w-full",
        "overflow-hidden rounded-lg",
        "border border-gray-200 dark:border-gray-700",
        className
      )}
    >
      <img
        src={data.image}
        alt="Matplotlib Plot"
        className="max-w-full max-h-[500px] object-contain"
        onError={(e) => {
          console.error("Error loading Matplotlib plot", e);
          onError?.(e);
        }}
      />
    </div>
  );
};

export default MatplotlibPlotWidget;

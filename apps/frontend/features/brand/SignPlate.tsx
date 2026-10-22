// The brand: a Brazilian warning sign (placa de advertência) with a paw.
// Shared by the map header, the report flow and generated icons.

export function PawSign({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true">
      <rect
        x="10"
        y="10"
        width="44"
        height="44"
        rx="5"
        transform="rotate(45 32 32)"
        fill="#ffce00"
        stroke="#1b1f3b"
        strokeWidth="4"
      />
      <g fill="#1b1f3b">
        <ellipse cx="32" cy="37" rx="7.5" ry="6.5" />
        <ellipse cx="23.5" cy="28.5" rx="3" ry="3.8" />
        <ellipse cx="29" cy="24" rx="3" ry="3.8" />
        <ellipse cx="35" cy="24" rx="3" ry="3.8" />
        <ellipse cx="40.5" cy="28.5" rx="3" ry="3.8" />
      </g>
    </svg>
  );
}

export function SignPlate() {
  return (
    <div className="flex shrink-0 items-center gap-2 whitespace-nowrap rounded-lg border-[3px] border-tinta bg-sinal py-1 pl-1.5 pr-3 shadow-[0_2px_0_var(--color-tinta)]">
      <PawSign size={30} />
      <span className="font-display text-[1.35rem] leading-none tracking-tight text-tinta">
        Alerta Patinha
      </span>
    </div>
  );
}

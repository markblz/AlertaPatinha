// The map's visual contract (docs/domain/location-privacy.md): an exact
// location is a pin; an approximate one is a hex cell with NO centre dot,
// because people read the centre of an uncertainty shape as the true spot.
export function PrecisionLegend() {
  return (
    <aside
      aria-label="Legenda de precisão"
      className="rounded-lg bg-papel/95 px-3 py-2 text-[0.8125rem] leading-tight text-tinta shadow-md"
    >
      <ul className="space-y-1">
        <li className="flex items-center gap-2">
          <svg width="16" height="16" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M10 1.5 17.4 5.75v8.5L10 18.5 2.6 14.25v-8.5z" fill="#4a4f6a33" stroke="#4a4f6a" strokeWidth="2" />
          </svg>
          Área aproximada
        </li>
        <li className="flex items-center gap-2">
          <svg width="16" height="16" viewBox="0 0 20 20" aria-hidden="true">
            <circle cx="10" cy="10" r="6" fill="#4a4f6a" stroke="#fff" strokeWidth="2" />
          </svg>
          Local exato
        </li>
      </ul>
    </aside>
  );
}

// The map's visual contract (docs/domain/location-privacy.md): an exact
// location is a pin; an approximate one is a hex cell with NO centre dot,
// because people read the centre of an uncertainty shape as the true spot.
export function PrecisionLegend() {
  return (
    <aside
      aria-label="Legenda de precisão"
      className="absolute bottom-6 left-4 rounded-xl bg-white/95 p-3 text-sm text-neutral-800 shadow-lg"
    >
      <p className="mb-2 font-semibold">Onde foi visto</p>
      <ul className="space-y-1.5">
        <li className="flex items-center gap-2">
          <svg width="18" height="22" viewBox="0 0 18 22" aria-hidden="true">
            <path
              d="M9 21s7-6.2 7-12A7 7 0 0 0 2 9c0 5.8 7 12 7 12z"
              fill="#e8590c"
              stroke="#fff"
              strokeWidth="1.5"
            />
          </svg>
          Local exato
        </li>
        <li className="flex items-center gap-2">
          <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">
            <path
              d="M10 1.5 17.4 5.75v8.5L10 18.5 2.6 14.25v-8.5z"
              fill="#e8590c33"
              stroke="#e8590c"
              strokeWidth="1.5"
            />
          </svg>
          Área aproximada
        </li>
      </ul>
    </aside>
  );
}

const ParameterCard = ({
  icon,
  label,
  value,
  unit,
  gradientFrom = "#f0f0f0",
  gradientTo = "#e0e0e0",
}) => {
  return (
    <div
      className="rounded-2xl shadow-md px-3 py-4 w-full text-center transition-transform duration-300 hover:scale-105"
      style={{
        background: `linear-gradient(to bottom right, ${gradientFrom}, ${gradientTo})`,
        color: "#111",
      }}
    >
      {/* Icône */}
      <div className="mb-3 flex justify-center">
        {icon && <img src={icon} alt={label} className="h-10 w-10 drop-shadow-sm" />}
      </div>

      {/* Valeur + Unité */}
      <div className="text-xl md:text-2xl font-bold text-gray-900">
        {value}
        {unit && (
          <span className="text-sm md:text-base font-semibold ml-1 text-gray-700">{unit}</span>
        )}
      </div>

      {/* Label */}
      <p className="text-sm md:text-base font-medium text-gray-800 mt-2">{label}</p>
    </div>
  );
};

export default ParameterCard;

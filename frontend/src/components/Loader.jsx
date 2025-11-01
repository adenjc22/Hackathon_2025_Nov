export default function Loader() {
  return (
    <div className="flex items-center justify-center p-6 text-brand-blue">
      <div className="w-5 h-5 border-2 border-brand-blue border-t-transparent rounded-full animate-spin mr-3"></div>
      <span className="text-base font-medium tracking-wide">
        Loading…
      </span>
    </div>
  );
}

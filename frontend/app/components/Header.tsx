export default function Header() {
  return (
    <header className="w-full bg-white shadow-md py-4 px-6 flex justify-between items-center">
      <h1 className="text-xl font-bold">Comijest</h1>

      <nav className="flex gap-4">
        <a href="/" className="hover:text-blue-600">Strona główna</a>
        <a href="/symptoms" className="hover:text-blue-600">Objawy</a>
        <a href="/about" className="hover:text-blue-600">O nas</a>
      </nav>
    </header>
  );
}

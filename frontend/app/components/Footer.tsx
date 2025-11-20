export default function Footer() {
  return (
    <footer className="w-full bg-white shadow-red-300 shadow-[0_-1px_4px] text-sm text-gray-800">
      <div className="bg-yellow-50 border-b border-yellow-200 m-4 px-6 py-4 rounded-3xl">
        <div className="max-w-5xl mx-auto flex items-start gap-3">
          <span className="text-lg leading-none mt-0.5">ℹ️</span>
          <p className="text-xs md:text-sm leading-relaxed">
            <strong>Comijest.com.pl</strong> nie stawia diagnozy medycznej i nie powinien
            zastępować oceny licencjonowanego lekarza. Dostarcza informacji pomocnych
            w podejmowaniu decyzji w oparciu o łatwo dostępne informacje o objawach. Jeśli
            masz jakiekolwiek pytania lub wątpliwości dotyczące wyniku diagnozy,
            skonsultuj się z lekarzem.
          </p>
        </div>
      </div>

      <div className="px-6 py-8 m-8">
        <div className="max-w-5xl mx-auto grid gap-8 md:grid-cols-3">
          <div>
            <h3 className="font-semibold mb-3 text-base">Comijest</h3>
            <ul className="space-y-1 text-sm">
              <li><a href="/about" className="hover:underline">O nas</a></li>
              <li><a href="/interview" className="hover:underline">Wywiad</a></li>
              <li><a href="/articles" className="hover:underline">Artykuły i porady</a></li>
              <li><a href="/encyclopedia" className="hover:underline">Encyklopedia zdrowia</a></li>
              <li><a href="/press" className="hover:underline">Materiały prasowe</a></li>
            </ul>
          </div>

          <div className="text-sm">
            <h3 className="font-semibold mb-3 text-base">Napisz do nas</h3>
            <p className="mb-2">
              <a
                href="mailto:contact@comijest.pl"
                className="text-red-500 hover:underline"
              >
                contact@comijest.pl
              </a>
            </p>
            <p className="mt-6">comijest © 2025</p>
          </div>

          <div className="text-sm">
            <h3 className="font-semibold mb-3 text-base">Dowiedz się więcej</h3>
            <p className="mb-2">
              Technologia oceny objawów i triżu zasilana przez
            </p>
            <p className="mb-2 font-semibold text-red-500">
              AI
            </p>
            <p className="mb-4">
              Aby uzyskać więcej informacji, sprawdź nasze:
            </p>
            <ul className="space-y-1">
              {/* <li>
                <a href="/cookies" className="text-blue-600 hover:underline">
                  Polityka Cookies
                </a>
              </li>
              <li>
                <a href="/privacy" className="text-blue-600 hover:underline">
                  Polityka prywatności
                </a>
              </li> */}
              <li>
                <a href="/terms" className="text-blue-600 hover:underline">
                  Warunki korzystania z usług
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}

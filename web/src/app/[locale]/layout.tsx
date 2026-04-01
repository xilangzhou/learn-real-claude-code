import type { Metadata } from "next";
import { I18nProvider } from "@/lib/i18n";
import { Header } from "@/components/layout/header";
import en from "@/i18n/messages/en.json";
import zh from "@/i18n/messages/zh.json";
import ja from "@/i18n/messages/ja.json";
import "../globals.css";

const locales = ["en", "zh", "ja"];
const metaMessages: Record<string, typeof en> = { en, zh, ja };
const SITE_URL = "https://learn.ownlab.app";
const OG_IMAGE = "/lrcc.png";

const ogLocales: Record<string, string> = {
  en: "en_US",
  zh: "zh_CN",
  ja: "ja_JP",
};

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const messages = metaMessages[locale] || metaMessages.en;
  const title = messages.meta?.title || "Learn Real Claude Code";
  const description =
    messages.meta?.description ||
    "Build an AI coding agent from scratch, one concept at a time";
  const pagePath = `/${locale}/`;

  return {
    metadataBase: new URL(SITE_URL),
    title,
    description,
    alternates: {
      canonical: pagePath,
      languages: {
        en: "/en/",
        zh: "/zh/",
        ja: "/ja/",
      },
    },
    openGraph: {
      type: "website",
      url: pagePath,
      siteName: "Learn Real Claude Code",
      title,
      description,
      locale: ogLocales[locale] || ogLocales.en,
      images: [
        {
          url: OG_IMAGE,
          alt: title,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [
        {
          url: OG_IMAGE,
          alt: title,
        },
      ],
    },
  };
}

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <html lang={locale} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: `
          (function() {
            var theme = localStorage.getItem('theme');
            if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
              document.documentElement.classList.add('dark');
            }
          })();
        `}} />
      </head>
      <body className="min-h-screen bg-[var(--color-bg)] text-[var(--color-text)] antialiased">
        <I18nProvider locale={locale}>
          <Header />
          <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            {children}
          </main>
        </I18nProvider>
      </body>
    </html>
  );
}

import { VERSION_META } from "@/lib/constants";
import { getTranslations } from "@/lib/i18n-server";

export function getVersionMetaText(locale: string, version: string) {
  const tSession = getTranslations(locale, "sessions");
  const tSubtitle = getTranslations(locale, "session_subtitles");
  const tCore = getTranslations(locale, "session_core_additions");
  const tInsight = getTranslations(locale, "session_key_insights");
  const fallback = VERSION_META[version];

  return {
    title: tSession(version) || fallback?.title || version,
    subtitle: tSubtitle(version) || fallback?.subtitle || "",
    coreAddition: tCore(version) || fallback?.coreAddition || "",
    keyInsight: tInsight(version) || fallback?.keyInsight || "",
  };
}

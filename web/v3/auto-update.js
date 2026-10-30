/* HAI ĐẤT: tự nhận bản website đã triển khai, không tải mã ngoài. */
(() => {
  "use strict";
  const script = document.currentScript;
  const meta = document.querySelector('meta[name="hai-dat-revision"]');
  const current = meta && meta.content;
  const isRevision = value => typeof value === "string" && /^[a-f0-9]{64}$/.test(value);
  if (!script || !script.src || !isRevision(current)) return;

  // Mã bản dựng website để người đọc biết trang đang mở; không phải số phiên bản học liệu.
  const footer = document.querySelector("footer");
  if (footer) {
    const label = document.createElement("p");
    label.className = "website-revision";
    label.textContent = "Mã bản website: " + current.slice(0, 12);
    (footer.querySelector(".container") || footer).append(label);
  }

  let manifest;
  try {
    const scriptUrl = new URL(script.src, window.location.href);
    // Chỉ tin manifest cùng nguồn với trang, kể cả khi thẻ script bị sửa.
    if (scriptUrl.origin !== window.location.origin) return;
    manifest = new URL("../../site-version.json", scriptUrl);
  } catch (_) {
    return;
  }

  const marker = "hai_dat_version";
  let checking = false;
  async function check() {
    if (checking || document.visibilityState === "hidden") return;
    checking = true;
    try {
      const response = await fetch(manifest.href, {cache: "no-store", redirect: "error"});
      if (!response.ok) return;
      const data = await response.json();
      if (!data || !isRevision(data.version) || data.version === current) return;
      const next = new URL(window.location.href);
      // Nếu CDN vẫn trả HTML cũ, chỉ tải lại một lần cho mã phiên bản này.
      // Tham số cũng phá cache HTML và URL API vẫn giữ những tham số khác và hash.
      if (next.searchParams.get(marker) === data.version) return;
      next.searchParams.set(marker, data.version);
      window.location.replace(next.href);
    } catch (_) {
      // Khi mất mạng hoặc manifest chưa sẵn sàng, giữ trang đang đọc và thử lại sau.
    } finally {
      checking = false;
    }
  }
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") void check();
  });
  window.setInterval(() => void check(), 60_000);
  void check();
})();

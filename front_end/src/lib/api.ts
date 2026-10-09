// 백엔드(FastAPI) 호출 기본 주소. 브라우저에서 쓰므로 NEXT_PUBLIC_ 접두사가 필요하다.
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8100";

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} 실패: ${res.status}`);
  return res.json() as Promise<T>;
}

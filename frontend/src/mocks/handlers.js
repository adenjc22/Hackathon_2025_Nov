import { http, HttpResponse } from "msw";

let fakeUser = { id: 1, email: "test@example.com", name: "Test User" };

let media = [
  { id: "1", fileName: "beach.jpg", fileUrl: "/demo/beach.jpg", mimeType: "image/jpeg", status: "done" },
  { id: "2", fileName: "party.mp4", fileUrl: "/demo/party.mp4", mimeType: "video/mp4", status: "processing" },
];

let albums = [
  { id: "a1", title: "Summer 2024", coverUrl: "/demo/beach.jpg", mediaCount: 42 },
];

export const handlers = [
  // ---------- Auth ----------
  http.post("/api/auth/signup", async ({ request }) => {
    const body = await request.json();
    fakeUser = { id: 1, ...body };
    return HttpResponse.json({ user: fakeUser });
  }),

  http.post("/api/auth/login", async ({ request }) => {
    const body = await request.json();
    if (body.email !== fakeUser.email) {
      return HttpResponse.json(
        { detail: "Invalid credentials" },
        { status: 401 }
      );
    }
    return HttpResponse.json({ user: fakeUser, accessToken: "mock.token" });
  }),

  http.get("/api/users/me", () => HttpResponse.json(fakeUser)),

  // ---------- Media ----------
  http.get("/api/upload/media", () => HttpResponse.json(media)),

  http.post("/api/upload/media", async ({ request }) => {
    const formData = await request.formData();
    const uploaded = [];

    for (const file of formData.getAll("files")) {
      const objectUrl = URL.createObjectURL(file);

      const newItem = {
        id: String(Date.now() + Math.random()), // unique-ish id
        fileName: file.name,
        fileUrl: objectUrl, // instant local preview
        mimeType: file.type,
        status: "pending",
      };

      uploaded.push(newItem);
      media.unshift(newItem);
    }

    // Simulate background processing finishing after 3 seconds
    setTimeout(() => {
      media = media.map((m) =>
        uploaded.find((u) => u.id === m.id)
          ? { ...m, status: "done" }
          : m
      );
    }, 3000);

    return HttpResponse.json(uploaded);
  }),

  http.delete("/api/upload/media/:id", ({ params }) => {
    const { id } = params;
    media = media.filter((m) => m.id !== id);
    return HttpResponse.json({ success: true });
  }), 


  // ---------- Albums ----------
  http.get("/api/albums", () => HttpResponse.json(albums)),

  // ---------- Search ----------
  http.get("/api/search", ({ request }) => {
    const q =
      new URL(request.url).searchParams.get("query")?.toLowerCase() ?? "";
    const results = media.filter((m) =>
      m.fileName.toLowerCase().includes(q)
    );
    return HttpResponse.json(results);
  }),
];

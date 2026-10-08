import heapq

INF = float("inf")


def fmt(x):
    return "∞" if x == INF else (str(int(x)) if x == int(x) else str(x))


def tabel(judul, header, baris):
    """Mencetak tabel dengan garis border."""
    semua = [header] + baris
    lebar = [max(len(str(r[i])) for r in semua) + 2 for i in range(len(header))]
    garis = "+" + "+".join("-" * w for w in lebar) + "+"

    def cetak_baris(r):
        print("|" + "|".join(str(c).center(w) for c, w in zip(r, lebar)) + "|")

    print(f"\n{judul}")
    print(garis)
    cetak_baris(header)
    print(garis)
    for r in baris:
        cetak_baris(r)
    print(garis)


def bangun_matriks(node, edges):
    idx = {n: i for i, n in enumerate(node)}
    m = [[INF] * len(node) for _ in node]
    for i in range(len(node)):
        m[i][i] = 0
    for a, b, w in edges:
        m[idx[a]][idx[b]] = w
        m[idx[b]][idx[a]] = w
    return m


def dijkstra(node, m, awal, tujuan):
    idx = {n: i for i, n in enumerate(node)}
    jarak = {n: INF for n in node}
    prev = {n: None for n in node}
    jarak[awal] = 0
    selesai = set()
    pq = [(0, awal)]
    langkah = []

    while pq:
        d, u = heapq.heappop(pq)
        if u in selesai:
            continue
        selesai.add(u)
        for v in node:
            w = m[idx[u]][idx[v]]
            if v != u and w != INF and v not in selesai and d + w < jarak[v]:
                jarak[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (jarak[v], v))
        langkah.append((u, dict(jarak)))
        if u == tujuan:
            break

    jalur, cur = [], tujuan
    while cur is not None:
        jalur.append(cur)
        cur = prev[cur]
    return jalur[::-1], jarak[tujuan], langkah


def proses(nama, node, edges, awal="A", tujuan="E"):
    print("\n" + "=" * 60)
    print(nama.center(60))
    print("=" * 60)
    m = bangun_matriks(node, edges)
    idx = {n: i for i, n in enumerate(node)}

    # Tabel 1: matriks jarak
    tabel("TABEL 1 - Matriks Jarak Langsung",
          [""] + node,
          [[n] + [fmt(v) for v in m[i]] for i, n in enumerate(node)])

    jalur, total, langkah = dijkstra(node, m, awal, tujuan)

    # Tabel 2: langkah Dijkstra
    tabel("TABEL 2 - Langkah Algoritma Dijkstra",
          ["Iterasi", "Dipilih"] + node,
          [[i + 1, u] + [fmt(j[n]) for n in node] for i, (u, j) in enumerate(langkah)])

    # Tabel 3: jalur optimal
    baris, kum = [], 0
    for a, b in zip(jalur, jalur[1:]):
        w = m[idx[a]][idx[b]]
        kum += w
        baris.append([f"{a} -> {b}", fmt(w), fmt(kum)])
    baris.append(["TOTAL", "", fmt(total)])
    tabel("TABEL 3 - Jalur Optimal", ["Rute", "Bobot", "Kumulatif"], baris)

    print(f"\nJalur terpendek {awal} -> {tujuan}: {' -> '.join(jalur)}  (total = {fmt(total)})")


if __name__ == "__main__":
    proses(
        "GRAF 1 (kiri)",
        ["A", "B", "C", "D", "E", "F"],
        [("A", "B", 4), ("A", "C", 6), ("B", "C", 2),
         ("B", "D", 9), ("C", "D", 8), ("D", "E", 9), ("B", "F", 2)],
    )
    proses(
        "GRAF 2 (kanan)",
        ["A", "B", "C", "D", "E"],
        [("A", "D", 6), ("A", "B", 7), ("A", "C", 8),
         ("B", "C", 0.5), ("D", "E", 11), ("C", "E", 1)],
    )

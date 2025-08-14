import java.util.*;

public class TestClass {

    static class Edge {
        int to, weight;
        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    static int time = 0;

    public static int getCheapestResult(int n, int k, int[][] arr) {
        List<List<Edge>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());

        for (int[] edge : arr) {
            int u = edge[0], v = edge[1], w = edge[2];
            graph.get(u).add(new Edge(v, w));
            graph.get(v).add(new Edge(u, w));
        }

        boolean[] visited = new boolean[n];
        int[] disc = new int[n];
        int[] low = new int[n];
        boolean[] isArticulation = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (!visited[i])
                dfsArticulation(i, -1, graph, visited, disc, low, isArticulation);
        }

        Set<Integer> validNodes = new HashSet<>();
        for (int i = 0; i < n; i++) {
            if (!isArticulation[i])
                validNodes.add(i);
        }

        List<List<Edge>> newGraph = new ArrayList<>();
        for (int i = 0; i < n; i++) newGraph.add(new ArrayList<>());

        for (int[] edge : arr) {
            int u = edge[0], v = edge[1], w = edge[2];
            if (validNodes.contains(u) && validNodes.contains(v)) {
                newGraph.get(u).add(new Edge(v, w));
                newGraph.get(v).add(new Edge(u, w));
            }
        }

        boolean[] mstVisited = new boolean[n];
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        int start = -1;

        for (int i = 0; i < n; i++) {
            if (!newGraph.get(i).isEmpty()) {
                start = i;
                break;
            }
        }

        if (start == -1) return 0;

        pq.offer(new int[]{start, 0});
        int totalCost = 0;

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int node = curr[0], cost = curr[1];

            if (mstVisited[node]) continue;
            mstVisited[node] = true;
            totalCost += cost;

            for (Edge edge : newGraph.get(node)) {
                if (!mstVisited[edge.to]) {
                    pq.offer(new int[]{edge.to, edge.weight});
                }
            }
        }

        return totalCost;
    }

    private static void dfsArticulation(int u, int parent, List<List<Edge>> graph,
                                        boolean[] visited, int[] disc, int[] low, boolean[] isArticulation) {
        visited[u] = true;
        disc[u] = low[u] = ++time;
        int children = 0;

        for (Edge e : graph.get(u)) {
            int v = e.to;
            if (!visited[v]) {
                children++;
                dfsArticulation(v, u, graph, visited, disc, low, isArticulation);
                low[u] = Math.min(low[u], low[v]);

                if (parent != -1 && low[v] >= disc[u])
                    isArticulation[u] = true;

            } else if (v != parent) {
                low[u] = Math.min(low[u], disc[v]);
            }
        }

        if (parent == -1 && children > 1)
            isArticulation[u] = true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[][] arr = new int[k][3];

        for (int i = 0; i < k; ++i) {
            arr[i][0] = sc.nextInt();
            arr[i][1] = sc.nextInt();
            arr[i][2] = sc.nextInt();
        }

        int result = getCheapestResult(n, k, arr);
        System.out.print(result);
    }
}
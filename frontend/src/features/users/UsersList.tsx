// src/features/users/UsersList.tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { UsersAPI, AuthAPI, buildPageParams } from "@/utils/api";

export default function UsersList() {
  const qc = useQueryClient();

  const users = useQuery({
    queryKey: ["users", { page: 1 }],
    queryFn: () => UsersAPI.list(buildPageParams({ page: 1, pageSize: 50 })),
  });

  const createUser = useMutation({
    mutationFn: () => UsersAPI.create({ email: "test@example.com", password: "Secret123!" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  });

  return (
    <div className="space-y-4">
      <button className="px-3 py-2 rounded-lg bg-blue-600 text-white"
              onClick={() => createUser.mutate()}>
        Create test user
      </button>

      {users.isLoading && <p>Loading…</p>}
      {users.isError && <p className="text-red-600">{(users.error as any)?.friendlyMessage}</p>}
      {users.data && (
        <ul className="list-disc pl-6">
          {users.data.map((u: any) => <li key={u.id}>{u.email}</li>)}
        </ul>
      )}
    </div>
  );
}

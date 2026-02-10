import { z } from "zod";
import type { NotebookLMClient } from "./client.js";

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: z.ZodType;
  handler: (client: NotebookLMClient, args: unknown) => Promise<unknown>;
}

export const tools: ToolDefinition[] = [
  // ── 노트북 관리 ──

  {
    name: "create_notebook",
    description:
      "새로운 NotebookLM 노트북을 생성합니다. 노트북 제목을 지정하세요.",
    inputSchema: z.object({
      title: z.string().describe("생성할 노트북의 제목"),
    }),
    handler: async (client, args) => {
      const { title } = args as { title: string };
      return client.createNotebook(title);
    },
  },

  {
    name: "get_notebook",
    description: "노트북 ID로 특정 노트북의 상세 정보를 조회합니다.",
    inputSchema: z.object({
      notebookId: z.string().describe("조회할 노트북의 ID"),
    }),
    handler: async (client, args) => {
      const { notebookId } = args as { notebookId: string };
      return client.getNotebook(notebookId);
    },
  },

  {
    name: "list_notebooks",
    description: "최근에 조회한 노트북 목록을 가져옵니다.",
    inputSchema: z.object({}),
    handler: async (client) => {
      return client.listRecentlyViewedNotebooks();
    },
  },

  {
    name: "delete_notebooks",
    description: "하나 이상의 노트북을 삭제합니다.",
    inputSchema: z.object({
      notebookIds: z
        .array(z.string())
        .describe("삭제할 노트북 ID 목록"),
    }),
    handler: async (client, args) => {
      const { notebookIds } = args as { notebookIds: string[] };
      await client.deleteNotebooks(notebookIds);
      return { success: true, deleted: notebookIds };
    },
  },

  {
    name: "share_notebook",
    description:
      "노트북을 다른 사용자와 공유합니다. 이메일과 역할(OWNER/WRITER/READER)을 지정하세요.",
    inputSchema: z.object({
      notebookId: z.string().describe("공유할 노트북의 ID"),
      shares: z
        .array(
          z.object({
            email: z.string().describe("공유 대상의 이메일 주소"),
            role: z
              .enum([
                "PROJECT_ROLE_OWNER",
                "PROJECT_ROLE_WRITER",
                "PROJECT_ROLE_READER",
              ])
              .describe("부여할 역할"),
          })
        )
        .describe("공유 대상 목록"),
    }),
    handler: async (client, args) => {
      const { notebookId, shares } = args as {
        notebookId: string;
        shares: Array<{
          email: string;
          role:
            | "PROJECT_ROLE_OWNER"
            | "PROJECT_ROLE_WRITER"
            | "PROJECT_ROLE_READER";
        }>;
      };
      await client.shareNotebook(notebookId, { accountAndRoles: shares });
      return { success: true, notebookId, sharedWith: shares };
    },
  },

  // ── 소스(데이터) 관리 ──

  {
    name: "add_drive_sources",
    description:
      "노트북에 Google Drive 문서(Google Docs, Slides 등)를 소스로 추가합니다.",
    inputSchema: z.object({
      notebookId: z.string().describe("소스를 추가할 노트북의 ID"),
      driveResourceIds: z
        .array(z.string())
        .describe("추가할 Google Drive 리소스 ID 목록"),
    }),
    handler: async (client, args) => {
      const { notebookId, driveResourceIds } = args as {
        notebookId: string;
        driveResourceIds: string[];
      };
      return client.addDriveSources(notebookId, driveResourceIds);
    },
  },

  {
    name: "upload_file_source",
    description:
      "로컬 파일을 노트북의 소스로 업로드합니다. base64로 인코딩된 파일 내용을 전달하세요.",
    inputSchema: z.object({
      notebookId: z.string().describe("파일을 업로드할 노트북의 ID"),
      fileName: z.string().describe("업로드할 파일의 이름"),
      fileContentBase64: z
        .string()
        .describe("base64로 인코딩된 파일 내용"),
    }),
    handler: async (client, args) => {
      const { notebookId, fileName, fileContentBase64 } = args as {
        notebookId: string;
        fileName: string;
        fileContentBase64: string;
      };
      const buffer = Buffer.from(fileContentBase64, "base64");
      return client.uploadFile(notebookId, fileName, buffer);
    },
  },

  {
    name: "delete_sources",
    description: "노트북에서 소스를 삭제합니다.",
    inputSchema: z.object({
      notebookId: z.string().describe("소스를 삭제할 노트북의 ID"),
      sourceNames: z
        .array(z.string())
        .describe("삭제할 소스의 전체 리소스 이름 목록"),
    }),
    handler: async (client, args) => {
      const { notebookId, sourceNames } = args as {
        notebookId: string;
        sourceNames: string[];
      };
      await client.deleteSources(notebookId, sourceNames);
      return { success: true, deleted: sourceNames };
    },
  },
];

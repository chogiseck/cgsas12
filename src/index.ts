#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { SearchServiceClient } from "@google-cloud/discoveryengine";
import { z } from "zod";
import { NotebookLMClient } from "./client.js";

// ── 환경 변수 ──
const PROJECT_ID = process.env.GOOGLE_CLOUD_PROJECT_ID ?? process.env.PROJECT_ID;
const PROJECT_NUMBER = process.env.GOOGLE_CLOUD_PROJECT_NUMBER;
const LOCATION = process.env.NOTEBOOKLM_LOCATION ?? "global";

if (!PROJECT_ID && !PROJECT_NUMBER) {
  console.error(
    "오류: GOOGLE_CLOUD_PROJECT_ID 또는 GOOGLE_CLOUD_PROJECT_NUMBER 환경 변수를 설정해주세요."
  );
  process.exit(1);
}

// ── 유효성 검사 스키마 (Zod) ──
const SearchArgumentsSchema = z.object({
  query: z.string().min(2),
  category: z.enum(["elementary_edu", "pottery", "zettelkasten", "obsidian"]),
  pageSize: z.number().min(1).max(100).optional().default(5),
  enableQueryExpansion: z.boolean().optional().default(true),
  returnSnippet: z.boolean().optional().default(true),
  maxExtractiveAnswerCount: z.number().min(0).max(5).optional().default(1),
  summaryResultCount: z.number().min(1).max(10).optional().default(5),
  includeCitations: z.boolean().optional().default(true),
});

const CreateNotebookSchema = z.object({
  title: z.string().min(1),
});

const GetNotebookSchema = z.object({
  notebookId: z.string().min(1),
});

const DeleteNotebooksSchema = z.object({
  notebookIds: z.array(z.string().min(1)).min(1),
});

const ShareNotebookSchema = z.object({
  notebookId: z.string().min(1),
  shares: z.array(
    z.object({
      email: z.string().email(),
      role: z.enum([
        "PROJECT_ROLE_OWNER",
        "PROJECT_ROLE_WRITER",
        "PROJECT_ROLE_READER",
      ]),
    })
  ),
});

const AddDriveSourcesSchema = z.object({
  notebookId: z.string().min(1),
  driveResourceIds: z.array(z.string().min(1)).min(1),
});

const UploadFileSourceSchema = z.object({
  notebookId: z.string().min(1),
  fileName: z.string().min(1),
  fileContentBase64: z.string().min(1),
});

const DeleteSourcesSchema = z.object({
  notebookId: z.string().min(1),
  sourceNames: z.array(z.string().min(1)).min(1),
});

// ── 클라이언트 초기화 ──
const discoveryClient = new SearchServiceClient();
const notebookClient = PROJECT_NUMBER
  ? new NotebookLMClient({ projectNumber: PROJECT_NUMBER, location: LOCATION })
  : null;

// ── MCP 서버 생성 ──
const server = new Server(
  { name: "notebooklm-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ── 도구 목록 정의 ──
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    // 검색 도구
    {
      name: "search_knowledge_base",
      description:
        "초등교육, 도예, 제텔카스텐, 옵시디언 등 전문 지식 베이스에서 정보를 검색합니다. 스니펫, 추출 답변, AI 요약을 포함한 결과를 반환합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          query: { type: "string", description: "검색어 (최소 2자)" },
          category: {
            type: "string",
            enum: ["elementary_edu", "pottery", "zettelkasten", "obsidian"],
            description: "지식 카테고리",
          },
          pageSize: {
            type: "number",
            description: "반환할 검색 결과 수 (기본값: 5, 최대: 100)",
          },
          enableQueryExpansion: {
            type: "boolean",
            description: "쿼리 자동 확장 활성화 (기본값: true)",
          },
          returnSnippet: {
            type: "boolean",
            description: "검색 결과에 스니펫 포함 (기본값: true)",
          },
          maxExtractiveAnswerCount: {
            type: "number",
            description: "추출 답변 최대 개수 (기본값: 1, 최대: 5)",
          },
          summaryResultCount: {
            type: "number",
            description: "요약에 포함할 결과 수 (기본값: 5, 최대: 10)",
          },
          includeCitations: {
            type: "boolean",
            description: "요약에 인용 포함 여부 (기본값: true)",
          },
        },
        required: ["query", "category"],
      },
    },
    // 노트북 관리 도구
    {
      name: "create_notebook",
      description: "새로운 NotebookLM 노트북을 생성합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          title: { type: "string", description: "노트북 제목" },
        },
        required: ["title"],
      },
    },
    {
      name: "get_notebook",
      description: "노트북 ID로 상세 정보를 조회합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          notebookId: { type: "string", description: "노트북 ID" },
        },
        required: ["notebookId"],
      },
    },
    {
      name: "list_notebooks",
      description: "최근에 조회한 노트북 목록을 가져옵니다.",
      inputSchema: {
        type: "object" as const,
        properties: {},
      },
    },
    {
      name: "delete_notebooks",
      description: "하나 이상의 노트북을 삭제합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          notebookIds: {
            type: "array",
            items: { type: "string" },
            description: "삭제할 노트북 ID 목록",
          },
        },
        required: ["notebookIds"],
      },
    },
    {
      name: "share_notebook",
      description: "노트북을 다른 사용자와 공유합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          notebookId: { type: "string", description: "노트북 ID" },
          shares: {
            type: "array",
            items: {
              type: "object",
              properties: {
                email: { type: "string", description: "이메일 주소" },
                role: {
                  type: "string",
                  enum: [
                    "PROJECT_ROLE_OWNER",
                    "PROJECT_ROLE_WRITER",
                    "PROJECT_ROLE_READER",
                  ],
                  description: "역할",
                },
              },
              required: ["email", "role"],
            },
            description: "공유 대상 목록",
          },
        },
        required: ["notebookId", "shares"],
      },
    },
    // 소스 관리 도구
    {
      name: "add_drive_sources",
      description: "노트북에 Google Drive 문서를 소스로 추가합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          notebookId: { type: "string", description: "노트북 ID" },
          driveResourceIds: {
            type: "array",
            items: { type: "string" },
            description: "Google Drive 리소스 ID 목록",
          },
        },
        required: ["notebookId", "driveResourceIds"],
      },
    },
    {
      name: "upload_file_source",
      description:
        "로컬 파일을 노트북의 소스로 업로드합니다. base64 인코딩된 내용을 전달하세요.",
      inputSchema: {
        type: "object" as const,
        properties: {
          notebookId: { type: "string", description: "노트북 ID" },
          fileName: { type: "string", description: "파일 이름" },
          fileContentBase64: {
            type: "string",
            description: "base64 인코딩된 파일 내용",
          },
        },
        required: ["notebookId", "fileName", "fileContentBase64"],
      },
    },
    {
      name: "delete_sources",
      description: "노트북에서 소스를 삭제합니다.",
      inputSchema: {
        type: "object" as const,
        properties: {
          notebookId: { type: "string", description: "노트북 ID" },
          sourceNames: {
            type: "array",
            items: { type: "string" },
            description: "소스 리소스 이름 목록",
          },
        },
        required: ["notebookId", "sourceNames"],
      },
    },
  ],
}));

// ── 도구 실행 핸들러 ──
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name } = request.params;
  const args = request.params.arguments;

  try {
    switch (name) {
      // ── 검색 ──
      case "search_knowledge_base": {
        const {
          query,
          category,
          pageSize,
          enableQueryExpansion,
          returnSnippet,
          maxExtractiveAnswerCount,
          summaryResultCount,
          includeCitations,
        } = SearchArgumentsSchema.parse(args);
        const projectId = PROJECT_ID ?? PROJECT_NUMBER;
        const [response] = await discoveryClient.search({
          servingConfig: `projects/${projectId}/locations/global/collections/default_collection/dataStores/${category}_ds/servingConfigs/default_search`,
          query,
          pageSize,
          queryExpansionSpec: {
            condition: enableQueryExpansion ? "AUTO" : "DISABLED",
          },
          contentSearchSpec: {
            snippetSpec: {
              returnSnippet,
            },
            extractiveContentSpec: {
              maxExtractiveAnswerCount,
            },
            summarySpec: {
              summaryResultCount,
              includeCitations,
            },
          },
        });
        return {
          content: [{ type: "text", text: JSON.stringify(response, null, 2) }],
        };
      }

      // ── 노트북 관리 ──
      case "create_notebook": {
        requireNotebookClient();
        const { title } = CreateNotebookSchema.parse(args);
        const result = await notebookClient!.createNotebook(title);
        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      }

      case "get_notebook": {
        requireNotebookClient();
        const { notebookId } = GetNotebookSchema.parse(args);
        const result = await notebookClient!.getNotebook(notebookId);
        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      }

      case "list_notebooks": {
        requireNotebookClient();
        const result = await notebookClient!.listRecentlyViewedNotebooks();
        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      }

      case "delete_notebooks": {
        requireNotebookClient();
        const { notebookIds } = DeleteNotebooksSchema.parse(args);
        await notebookClient!.deleteNotebooks(notebookIds);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, deleted: notebookIds }, null, 2),
            },
          ],
        };
      }

      case "share_notebook": {
        requireNotebookClient();
        const { notebookId, shares } = ShareNotebookSchema.parse(args);
        await notebookClient!.shareNotebook(notebookId, {
          accountAndRoles: shares,
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, notebookId, sharedWith: shares }, null, 2),
            },
          ],
        };
      }

      // ── 소스 관리 ──
      case "add_drive_sources": {
        requireNotebookClient();
        const { notebookId, driveResourceIds } = AddDriveSourcesSchema.parse(args);
        const result = await notebookClient!.addDriveSources(notebookId, driveResourceIds);
        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      }

      case "upload_file_source": {
        requireNotebookClient();
        const { notebookId, fileName, fileContentBase64 } =
          UploadFileSourceSchema.parse(args);
        const buffer = Buffer.from(fileContentBase64, "base64");
        const result = await notebookClient!.uploadFile(notebookId, fileName, buffer);
        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      }

      case "delete_sources": {
        requireNotebookClient();
        const { notebookId, sourceNames } = DeleteSourcesSchema.parse(args);
        await notebookClient!.deleteSources(notebookId, sourceNames);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, deleted: sourceNames }, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`도구를 찾을 수 없습니다: ${name}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [{ type: "text", text: `오류 발생: ${message}` }],
      isError: true,
    };
  }
});

function requireNotebookClient(): void {
  if (!notebookClient) {
    throw new Error(
      "노트북 관리 기능을 사용하려면 GOOGLE_CLOUD_PROJECT_NUMBER 환경 변수를 설정해주세요."
    );
  }
}

// ── 서버 실행 ──
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("NotebookLM MCP 서버가 시작되었습니다.");
}

main().catch((error) => {
  console.error("서버 시작 실패:", error);
  process.exit(1);
});

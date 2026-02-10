#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { NotebookLMClient } from "./client.js";
import { tools } from "./tools.js";

const projectNumber = process.env.GOOGLE_CLOUD_PROJECT_NUMBER;
const location = process.env.NOTEBOOKLM_LOCATION ?? "global";

if (!projectNumber) {
  console.error(
    "오류: GOOGLE_CLOUD_PROJECT_NUMBER 환경 변수를 설정해주세요."
  );
  process.exit(1);
}

const client = new NotebookLMClient({ projectNumber, location });

const server = new McpServer({
  name: "notebooklm-mcp",
  version: "1.0.0",
});

// 도구 등록
for (const tool of tools) {
  const shape: Record<string, z.ZodType> = {};
  if (tool.inputSchema instanceof z.ZodObject) {
    Object.assign(
      shape,
      (tool.inputSchema as z.ZodObject<Record<string, z.ZodType>>).shape
    );
  }

  server.tool(
    tool.name,
    tool.description,
    shape,
    async (args) => {
      try {
        const result = await tool.handler(client, args);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        const message =
          error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: "text" as const,
              text: `오류 발생: ${message}`,
            },
          ],
          isError: true,
        };
      }
    }
  );
}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("NotebookLM MCP 서버가 시작되었습니다.");
}

main().catch((error) => {
  console.error("서버 시작 실패:", error);
  process.exit(1);
});

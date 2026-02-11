import { GoogleAuth } from "google-auth-library";
import type {
  NotebookLMConfig,
  Notebook,
  NotebookSource,
  ShareRequest,
  BatchCreateSourcesRequest,
  BatchDeleteSourcesRequest,
  ListRecentlyViewedResponse,
} from "./types.js";

export class NotebookLMClient {
  private auth: GoogleAuth;
  private config: NotebookLMConfig;

  constructor(config: NotebookLMConfig) {
    this.config = config;
    this.auth = new GoogleAuth({
      scopes: ["https://www.googleapis.com/auth/cloud-platform"],
    });
  }

  private get baseUrl(): string {
    return `https://${this.config.location}-discoveryengine.googleapis.com/v1alpha/projects/${this.config.projectNumber}/locations/${this.config.location}`;
  }

  private async getHeaders(): Promise<Record<string, string>> {
    const client = await this.auth.getClient();
    const token = await client.getAccessToken();
    return {
      Authorization: `Bearer ${token.token}`,
      "Content-Type": "application/json",
    };
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers = await this.getHeaders();

    const options: RequestInit = {
      method,
      headers,
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `NotebookLM API error (${response.status}): ${errorText}`
      );
    }

    const text = await response.text();
    return text ? (JSON.parse(text) as T) : ({} as T);
  }

  // ── Notebook 관리 ──

  async createNotebook(title: string): Promise<Notebook> {
    return this.request<Notebook>("POST", "/notebooks", {
      displayName: title,
    });
  }

  async getNotebook(notebookId: string): Promise<Notebook> {
    return this.request<Notebook>("GET", `/notebooks/${notebookId}`);
  }

  async listRecentlyViewedNotebooks(): Promise<ListRecentlyViewedResponse> {
    return this.request<ListRecentlyViewedResponse>(
      "GET",
      "/notebooks:listRecentlyViewed"
    );
  }

  async deleteNotebooks(notebookIds: string[]): Promise<void> {
    const names = notebookIds.map(
      (id) =>
        `projects/${this.config.projectNumber}/locations/${this.config.location}/notebooks/${id}`
    );
    await this.request("POST", "/notebooks:batchDelete", { names });
  }

  async shareNotebook(
    notebookId: string,
    shareRequest: ShareRequest
  ): Promise<void> {
    await this.request(
      "POST",
      `/notebooks/${notebookId}:share`,
      shareRequest
    );
  }

  // ── Source(소스) 관리 ──

  async addDriveSources(
    notebookId: string,
    driveResourceIds: string[]
  ): Promise<NotebookSource[]> {
    const body: BatchCreateSourcesRequest = {
      requests: driveResourceIds.map((resourceId) => ({
        source: {
          driveSource: { resourceId },
        },
      })),
    };
    const result = await this.request<{ sources: NotebookSource[] }>(
      "POST",
      `/notebooks/${notebookId}/sources:batchCreate`,
      body
    );
    return result.sources ?? [];
  }

  async uploadFile(
    notebookId: string,
    fileName: string,
    fileContent: Buffer
  ): Promise<NotebookSource> {
    const url = `https://${this.config.location}-discoveryengine.googleapis.com/upload/v1alpha/projects/${this.config.projectNumber}/locations/${this.config.location}/notebooks/${notebookId}/sources:uploadFile`;
    const headers = await this.getHeaders();

    const boundary = "----MCP_UPLOAD_BOUNDARY";
    const metadata = JSON.stringify({ displayName: fileName });

    const bodyParts = [
      `--${boundary}\r\n`,
      'Content-Type: application/json; charset=UTF-8\r\n\r\n',
      `${metadata}\r\n`,
      `--${boundary}\r\n`,
      `Content-Type: application/octet-stream\r\n\r\n`,
    ];

    const bodyStart = Buffer.from(bodyParts.join(""));
    const bodyEnd = Buffer.from(`\r\n--${boundary}--\r\n`);
    const fullBody = Buffer.concat([bodyStart, fileContent, bodyEnd]);

    const response = await fetch(url, {
      method: "POST",
      headers: {
        ...headers,
        "Content-Type": `multipart/related; boundary=${boundary}`,
      },
      body: fullBody,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `NotebookLM upload error (${response.status}): ${errorText}`
      );
    }

    return (await response.json()) as NotebookSource;
  }

  async deleteSources(
    notebookId: string,
    sourceNames: string[]
  ): Promise<void> {
    const body: BatchDeleteSourcesRequest = { names: sourceNames };
    await this.request(
      "POST",
      `/notebooks/${notebookId}/sources:batchDelete`,
      body
    );
  }
}

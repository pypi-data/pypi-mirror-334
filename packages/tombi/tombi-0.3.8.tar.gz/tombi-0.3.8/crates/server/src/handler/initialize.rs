use tower_lsp::lsp_types::{
    ClientCapabilities, ClientInfo, CompletionOptions, CompletionOptionsCompletionItem,
    DiagnosticOptions, DiagnosticServerCapabilities, FoldingRangeProviderCapability,
    HoverProviderCapability, InitializeParams, InitializeResult, OneOf, PositionEncodingKind,
    SemanticTokenModifier, SemanticTokensFullOptions, SemanticTokensLegend, SemanticTokensOptions,
    ServerCapabilities, ServerInfo, TextDocumentSyncCapability, TextDocumentSyncKind,
    TextDocumentSyncOptions, TextDocumentSyncSaveOptions,
};

use crate::semantic_tokens::SUPPORTED_TOKEN_TYPES;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_initialize(
    InitializeParams {
        capabilities: client_capabilities,
        client_info,
        ..
    }: InitializeParams,
) -> Result<InitializeResult, tower_lsp::jsonrpc::Error> {
    let _p = tracing::debug_span!("handle_initialize").entered();

    if let Some(ClientInfo { name, version }) = client_info {
        let version = version.unwrap_or_default();
        tracing::info!("{name} version: {version}",);
    }

    Ok(InitializeResult {
        server_info: Some(ServerInfo {
            name: String::from("Tombi LSP"),
            version: Some(env!("CARGO_PKG_VERSION").to_string()),
        }),
        capabilities: server_capabilities(&client_capabilities),
    })
}

pub fn server_capabilities(client_capabilities: &ClientCapabilities) -> ServerCapabilities {
    ServerCapabilities {
        position_encoding: Some(PositionEncodingKind::UTF16),
        text_document_sync: Some(TextDocumentSyncCapability::Options(
            TextDocumentSyncOptions {
                open_close: Some(true),
                change: Some(TextDocumentSyncKind::FULL),
                save: Some(TextDocumentSyncSaveOptions::Supported(true)),
                ..Default::default()
            },
        )),
        hover_provider: Some(HoverProviderCapability::Simple(true)),
        completion_provider: Some(CompletionOptions {
            trigger_characters: Some(vec![
                ".".into(),
                ",".into(),
                "=".into(),
                "[".into(),
                "{".into(),
                " ".into(),
                "\n".into(),
            ]),
            completion_item: Some(CompletionOptionsCompletionItem {
                label_details_support: (|| -> _ {
                    client_capabilities
                        .text_document
                        .as_ref()?
                        .completion
                        .as_ref()?
                        .completion_item
                        .as_ref()?
                        .label_details_support
                })(),
            }),
            ..Default::default()
        }),
        // declaration_provider: Some(DeclarationCapability::Simple(true)),
        // definition_provider: Some(OneOf::Left(true)),
        // type_definition_provider: Some(TypeDefinitionProviderCapability::Simple(true)),
        // implementation_provider: Some(ImplementationProviderCapability::Simple(true)),
        // references_provider: Some(OneOf::Left(true)),
        document_symbol_provider: Some(OneOf::Left(true)),
        // workspace_symbol_provider: Some(OneOf::Left(true)),
        // code_lens_provider: Some(CodeLensOptions {
        //     resolve_provider: Some(true),
        // }),
        document_formatting_provider: Some(OneOf::Left(true)),
        // selection_range_provider: Some(SelectionRangeProviderCapability::Simple(true)),
        folding_range_provider: Some(FoldingRangeProviderCapability::Simple(true)),
        // rename_provider: Some(OneOf::Right(RenameOptions {
        //     prepare_provider: Some(true),
        //     work_done_progress_options: WorkDoneProgressOptions {
        //         work_done_progress: None,
        //     },
        // })),
        // workspace: Some(WorkspaceServerCapabilities {
        //     workspace_folders: Some(WorkspaceFoldersServerCapabilities {
        //         supported: Some(true),
        //         change_notifications: Some(OneOf::Left(true)),
        //     }),
        //     file_operations: None,
        // }),
        // call_hierarchy_provider: Some(CallHierarchyServerCapability::Simple(true)),
        semantic_tokens_provider: Some(
            SemanticTokensOptions {
                legend: SemanticTokensLegend {
                    token_types: SUPPORTED_TOKEN_TYPES.to_vec(),
                    token_modifiers: vec![SemanticTokenModifier::READONLY],
                },
                full: Some(SemanticTokensFullOptions::Bool(true)),
                ..Default::default()
            }
            .into(),
        ),
        // inlay_hint_provider: Some(OneOf::Right(InlayHintServerCapabilities::Options(
        //     InlayHintOptions {
        //         work_done_progress_options: Default::default(),
        //         resolve_provider: Some(true),
        //     },
        // ))),
        diagnostic_provider: Some(DiagnosticServerCapabilities::Options(DiagnosticOptions {
            ..Default::default()
        })),

        ..Default::default()
    }
}

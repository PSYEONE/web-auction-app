<template>
  <div class="qa-section">
    <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 2px solid var(--win-dark-gray);">
      <h3 style="margin-bottom: 12px;">Ask a Question</h3>
      <form @submit.prevent="submitQuestion">
        <textarea
            v-model="questionText"
            class="input-retro"
            placeholder="Type your question here..."
            rows="3"
            style="resize: vertical; margin-bottom: 8px;"
            required
        ></textarea>
        <button
            type="submit"
            class="btn-retro"
            :disabled="itemsStore.loading"
        >
          {{ itemsStore.loading ? 'Posting...' : 'Post Question' }}
        </button>
      </form>
      <p v-if="questionError" style="color: red; margin-top: 8px;">
        {{ questionError }}
      </p>
    </div>

    <div>
      <h3 style="margin-bottom: 12px;">All Questions ({{ item.questions.length }})</h3>
      <div v-if="item.questions.length === 0" style="padding: 20px; text-align: center; color: var(--win-dark-gray);">
        No questions yet. Be the first to ask!
      </div>
      <div v-else>
        <div
            v-for="question in sortedQuestions"
            :key="question.id"
            class="question-item"
        >
          <div style="margin-bottom: 8px;">
            <strong>{{ question.author.username }}:</strong> {{ question.question_text }}
            <br />
            <span style="font-size: 11px; color: var(--win-dark-gray);">
              {{ formatDate(question.timestamp) }}
            </span>
          </div>

          <div v-if="question.reply_text" class="reply-box">
            <strong>Reply:</strong> {{ question.reply_text }}
            <br />
            <span style="font-size: 11px; color: var(--win-dark-gray);">
              {{ formatDate(question.reply_timestamp!) }}
            </span>
          </div>

          <div v-else style="margin-top: 8px;">
            <div v-if="!currentUserId" style="color: var(--win-dark-gray); font-style: italic; font-size: 12px;">
              <a href="/login/" style="color: blue;">Log in</a> to reply or ask questions
            </div>
            <div v-else-if="isOwner">
              <form @submit.prevent="submitReply(question.id)">
                <textarea
                    v-model="replyTexts[question.id]"
                    class="input-retro"
                    placeholder="Type your reply as the item owner..."
                    rows="2"
                    style="resize: vertical; margin-bottom: 4px;"
                    required
                ></textarea>
                <button type="submit" class="btn-retro" style="font-size: 12px;">
                  Post Reply
                </button>
              </form>
            </div>
            <div v-else style="color: var(--win-dark-gray); font-style: italic; font-size: 12px;">
              Awaiting owner's reply...
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import type { Item, Question } from '../../types/models';
import { useItemsStore } from '../../stores/items';

export default defineComponent({
  name: 'QuestionAnswer',
  props: {
    item: {
      type: Object as PropType<Item>,
      required: true,
    },
    currentUserId: {
      type: Number,
      default: null,
    },
  },
  emits: ['question-posted', 'reply-posted'],
  data() {
    return {
      itemsStore: useItemsStore(),
      questionText: '',
      questionError: null as string | null,
      replyTexts: {} as Record<number, string>,
    };
  },
  computed: {
    isOwner(): boolean {
      return this.currentUserId === this.item.owner.id;
    },
    sortedQuestions(): Question[] {
      return [...this.item.questions].sort((a, b) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );
    },
  },
  methods: {
    async submitQuestion(): Promise<void> {
      this.questionError = null;
      try {
        await this.itemsStore.postQuestion(this.item.id, {
          question_text: this.questionText,
        });
        this.questionText = '';
        this.$emit('question-posted');
      } catch (e) {
        this.questionError = e instanceof Error ? e.message : 'Failed to post question';
      }
    },
    async submitReply(questionId: number): Promise<void> {
      try {
        await this.itemsStore.replyQuestion(questionId, {
          reply_text: this.replyTexts[questionId],
        });
        this.replyTexts[questionId] = '';
        this.$emit('reply-posted');
      } catch (e) {
        alert('Failed to post reply: ' + (e instanceof Error ? e.message : 'Unknown error'));
      }
    },
    formatDate(dateString: string): string {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
  },
});
</script>